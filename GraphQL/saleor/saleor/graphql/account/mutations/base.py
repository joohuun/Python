from itertools import chain
from typing import Tuple, Union

import graphene
from django.core.exceptions import (
    NON_FIELD_ERRORS,
    ImproperlyConfigured,
    ValidationError,
)
from django.db.models.fields.files import FileField
from graphene import ObjectType
from graphene.types.mutation import MutationOptions
from graphene_django.registry import get_global_registry
from graphql.error import GraphQLError

# from ...core.exceptions import PermissionDenied
# from ...core.permissions import AccountPermissions
from saleor.account.permissions import AccountPermissions

from ..utils import get_nodes
from .types import Error, Upload
from .utils import from_global_id_strict_type, snake_to_camel_case
from .utils.error_codes import get_error_code_from_error11

registry = get_global_registry()


class BaseMutation(graphene.Mutation):
    errors = graphene.List(
        graphene.NonNull(Error),
        description="List of errors that occurred executing the mutation.",
        deprecation_reason=(
            "Use typed errors with error codes. This field will be removed after "
            "2020-07-31."
        ),
        required=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        description=None,
        permissions: Tuple = None,
        _meta=None,
        error_type_class=None,
        error_type_field=None,
        errors_mapping=None,
        **options,
    ):
        if not _meta:
            _meta = MutationOptions(cls)

        if not description:
            raise ImproperlyConfigured("No description provided in Meta")

        if isinstance(permissions, str):
            permissions = (permissions,)

        if permissions and not isinstance(permissions, tuple):
            raise ImproperlyConfigured(
                "Permissions should be a tuple or a string in Meta"
            )

        _meta.permissions = permissions
        _meta.error_type_class = error_type_class
        _meta.error_type_field = error_type_field
        _meta.errors_mapping = errors_mapping
        super().__init_subclass_with_meta__(
            description=description, _meta=_meta, **options
        )
        if error_type_class and error_type_field:
            cls._meta.fields.update(
                get_error_fields(error_type_class, error_type_field)
            )

    @classmethod
    def _update_mutation_arguments_and_fields(cls, arguments, fields):
        cls._meta.arguments.update(arguments)
        cls._meta.fields.update(fields)

    @classmethod
    def get_node_by_pk(
        cls, info, graphene_type: ObjectType, pk: Union[int, str], qs=None
    ):
        """Attempt to resolve a node from the given internal ID.

        Whether by using the provided query set object or by calling type's get_node().
        """
        if qs is not None:
            return qs.filter(pk=pk).first()
        get_node = getattr(graphene_type, "get_node", None)
        if get_node:
            return get_node(info, pk)
        return None

    @classmethod
    def get_node_or_error(cls, info, node_id, field="id", only_type=None, qs=None):
        if not node_id:
            return None

        try:
            if only_type is not None:
                pk = from_global_id_strict_type(node_id, only_type, field=field)
            else:
                # FIXME: warn when supplied only_type is None?
                only_type, pk = graphene.Node.from_global_id(node_id)

            if isinstance(only_type, str):
                only_type = info.schema.get_type(only_type).graphene_type

            node = cls.get_node_by_pk(info, graphene_type=only_type, pk=pk, qs=qs)
        except (AssertionError, GraphQLError) as e:
            raise ValidationError(
                {field: ValidationError(str(e), code="graphql_error")}
            )
        else:
            if node is None:
                raise ValidationError(
                    {
                        field: ValidationError(
                            "Couldn't resolve to a node: %s" % node_id, code="not_found"
                        )
                    }
                )
        return node

    @classmethod
    def get_nodes_or_error(cls, ids, field, only_type=None, qs=None):
        try:
            instances = get_nodes(ids, only_type, qs=qs)
        except GraphQLError as e:
            raise ValidationError(
                {field: ValidationError(str(e), code="graphql_error")}
            )
        return instances

    @staticmethod
    def remap_error_fields(validation_error, field_map):
        """Rename validation_error fields accoring to provided field_map.

        Skips renaming fields from field_map that are not on validation_error.
        """
        for old_field, new_field in field_map.items():
            try:
                validation_error.error_dict[
                    new_field
                ] = validation_error.error_dict.pop(old_field)
            except KeyError:
                pass

    @classmethod
    def clean_instance(cls, info, instance):
        """Clean the instance that was created using the input data.

        Once an instance is created, this method runs `full_clean()` to perform
        model validation.
        """
        try:
            instance.full_clean()
        except ValidationError as error:
            if hasattr(cls._meta, "exclude"):
                # Ignore validation errors for fields that are specified as
                # excluded.
                new_error_dict = {field: errors for field, errors in error.error_dict.items() if field not in cls._meta.exclude}

                error.error_dict = new_error_dict

            if cls._meta.errors_mapping:
                cls.remap_error_fields(error, cls._meta.errors_mapping)

            if error.error_dict:
                raise error

    @classmethod
    def construct_instance(cls, instance, cleaned_data):
        """Fill instance fields with cleaned data.

        The `instance` argument is either an empty instance of a already
        existing one which was fetched from the database. `cleaned_data` is
        data to be set in instance fields. Returns `instance` with filled
        fields, but not saved to the database.
        """
        from django.db import models

        opts = instance._meta

        for f in opts.fields:
            if any(
                [
                    not f.editable,
                    isinstance(f, models.AutoField),
                    f.name not in cleaned_data,
                ]
            ):
                continue
            data = cleaned_data[f.name]
            if data is None:
                # We want to reset the file field value when None was passed
                # in the input, but `FileField.save_form_data` ignores None
                # values. In that case we manually pass False which clears
                # the file.
                if isinstance(f, FileField):
                    data = False
                if not f.null:
                    data = f._get_default()
            f.save_form_data(instance, data)
        return instance

    @classmethod
    def check_permissions(cls, context, permissions=None):
        """Determine whether user or app has rights to perform this mutation.

        Default implementation assumes that account is allowed to perform any
        mutation. By overriding this method or defining required permissions
        in the meta-class, you can restrict access to it.

        The `context` parameter is the Context instance associated with the request.
        """
        permissions = permissions or cls._meta.permissions
        if not permissions:
            return True
        if context.user.has_perms(permissions):
            return True
        app = getattr(context, "app", None)
        if app:
            # for now MANAGE_STAFF permission for app is not supported
            if AccountPermissions.MANAGE_STAFF in permissions:
                return False
            return app.has_perms(permissions)
        return False

    @classmethod
    def mutate(cls, root, info, **data):
        if not cls.check_permissions(info.context):
            raise PermissionDenied()

        try:
            response = cls.perform_mutation(root, info, **data)
            if response.errors is None:
                response.errors = []
            return response
        except ValidationError as e:
            return cls.handle_errors(e)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass

    @classmethod
    def handle_errors(cls, error: ValidationError, **extra):
        errors = validation_error_to_error_type(error)
        return cls.handle_typed_errors(errors, **extra)

    @classmethod
    def handle_typed_errors(cls, errors: list, **extra):
        """Return class instance with errors."""
        if (
            cls._meta.error_type_class is not None
            and cls._meta.error_type_field is not None
        ):
            typed_errors = []
            error_class_fields = set(cls._meta.error_type_class._meta.fields.keys())
            for e, code, params in errors:
                error_instance = cls._meta.error_type_class(
                    field=e.field, message=e.message, code=code
                )
                if params:
                    # If some of the params key overlap with error class fields
                    # attach param value to the error
                    error_fields_in_params = set(params.keys()) & error_class_fields
                    for error_field in error_fields_in_params:
                        setattr(error_instance, error_field, params[error_field])
                typed_errors.append(error_instance)

            extra.update({cls._meta.error_type_field: typed_errors})
        return cls(errors=[e[0] for e in errors], **extra)