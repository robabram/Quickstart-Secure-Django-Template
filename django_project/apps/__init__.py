

def PrepModalDialogFieldErrorMsg(msg):
    """
    Format the message so it looks just like a regular django html form field error
    :param msg:
    :return: formatted message
    """

    if not msg:
        return None

    return '<ul class="errorlist"><li>{0}</li></ul>'.format(msg)


def FormatModalDialogErrors(form):
    """
    Lump form field errors into one UL tag for modal dialog
    :param: form: form object
    :param: model: model
    """

    errors = ''
    for field in form.fields:
        if field in form.errors:
            # grab error html and insert field name. Try using model field information if available.
            # If it is not a model field, just use the field name we have.
            try:
                errors += str(form.errors[field]).replace(
                    '<ul class="errorlist"><li>', '<ul class="errorlist"><li>{0}: '.format(
                        form._meta.model._meta.get_field(field).verbose_name
                    ))
            except:
                errors += str(form.errors[field]).replace(
                    '<ul class="errorlist"><li>', '<ul class="errorlist"><li>{0}: '.format(str(field))
                )

    # Remove middle ul tags so this is just one big ul list
    errors = errors.replace('</ul><ul class="errorlist">', '')

    return errors

