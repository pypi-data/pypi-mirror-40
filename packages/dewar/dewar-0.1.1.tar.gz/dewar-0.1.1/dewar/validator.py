from dewar.exceptions import ValidationError

def validate_dict(val, path_elements):
    def has_correct_key(key):
        return isinstance(key, tuple) or isinstance(key, str)

    def is_allowed_single(key):
        return len(path_elements) == 1 or isinstance(key, tuple)


def validate_page(val):
    path_elements = parse_path(wrapper.path)
    if str(val) == val:
        if path_elements:
            raise ValidationError(f"{wrapper.name}'s path requires variables, which were not provided.")
    elif type(val) is dict:
        if path_elements is None:
            raise ValidationError("{wrapper.name}'s path did not specify variables, but returned variables anyway.")
        validate_dict(val, path_elements)
    else:
        raise ValidationError(f"{wrapper.name} did not return a valid object to construct the page.")
