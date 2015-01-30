# Frasco-Forms

Provides forms creation and management to your application using [WTForms](http://wtforms.readthedocs.org/)
and [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/).

## Installation

    pip install frasco-forms

## Setup

Feature name: forms

Options:

 - *upload_backend*: the backend to use when uploading files (default: local)
 - *upload_dir*: the directory where uploaded files will be saved when using the local backend (default: uploads)
 - *upload_url*: base url path for uploaded files (default: /uploads)
 - *upload_uuid_prefixes*: whether to prepend an UUID to the filename of uploaded files (default: True)
 - *upload_keep_filenames*: whether to keep the original filename in the uploaded file's filename (default: True)
 - *upload_subfolders*: whether to use a subfolders structure to store uploaded files when using
   This is useful when many files are planned to be uploaded as some OSes have limits on the number
   of files inside a single folder (default: False)
 - *csrf_enabled*: whether to enable Cross Site Request Forgery protection (default: True)
 - *import_macros*: import macros provided by the feature (default: True)

## Actions

### form

Initialize an instance of the specified form and validates when a POST request is submitted.
If no name is provider or if it does not reference an existing form, the form will be built using
using the template.

See the "Defining forms in template" section.

Depending on the result of the validation (unless *validate_on_submit* is False), an action
group will be triggered: if successful, *form_submitted* is triggered, if failed,
*form_validation_failed* is triggered.

Options:

 - *name* (default): the name of the form to use (optional)
 - *obj*: an object to pre-fill the form with (optional)
 - *template*: the filename of the template where the form is defined (optional)
 - *var_name*: the variable name of the form instance when building the form from a template (optional)
 - *validate_on_submit*: whether to automatically validate the form when the request method is POST (default: True)
 - *exit_on_failure*: whether to exit the context on validation failure (default: True)
 - *csrf_enabled*: whether to enable Cross Site Request Forgery protection (default: the value of the csrf_enabled option)

Returns a form instance
Default variable assignment: `$form`

### create\_form\_from\_view

Creates a form from information in the view from which the action is called

Options:

 - *name* (default): the name of the form to use
 - *var_name*: the variable name of the form instance (optional)

Returns a form class
Default variable assignment: `$form_class`

### create\_form\_from\_template

Creates a form from information in the specified template

Options:

 - *name*: the name of the form to use
 - *template*: the filename of the template where the form is defined
 - *var_name*: the variable name of the form instance (default: form)

Returns a form class
Default variable assignment: `$form_class`

### validate\_form

Validates the current or specified form.

Depending on the result of the validation (unless *return_success* is True), an action
group will be triggered: if successful, *form_submitted* is triggered, if failed,
*form_validation_failed* is triggered.

Options:

 - *form* (default): the form instance (default: the current form)
 - *return_success*: whether to return a boolean instead of triggering an action group (default: False)
 - *exit_on_failure*: whether to exit the context on failure (default: True)

### form\_to\_obj

Populates an object with the form's data.

Options:

 - *obj* (default): an object (default: a new instance of `frasco.utils.AttrDict`)
 - *form*: the form instance (default: the current form)

## Defining forms in templates

Frasco-Forms gives you the possibility to quickly define forms directly in the
template.

When the *form* action is used without a *name* option or with one not referencing
an existing form class, a form class will be created from the view's template.

Defining forms is almost like using a pre-defined form but with added information
on the type of the field.

To do so, you'll need to call a method named after the type of the field on each
field. So if you want to define a "firstname" field as a text field, you can
do `form.firstname.text()`.

Let's define a signup form:

    <form action="" method="post">
        {{ form.csrf_token() }}
        <p><label>First name</label> {{ form.firstname.text() }}</p>
        <p><label>Last name</label> {{ form.lastname.text() }}</p>
        <p><label>Email</label> {{ form.email.email() }}</p>
        <p><label>Password</label> {{ form.password.password() }}</p>
    </form>

The optional parameters of the field definition functions are:

 - *label*: the field's label (can also be define as the first argument)
 - *description*: the field's description
 - *required*: boolean, default false
 - *optional*: boolean, default false
 - *range*: a tuple of (min, max), value should be a number in the range
 - *length*: a tuple of (min, max), value should be of string of length in the range
 - *validators*: a list of validator names from `wtforms.validators`

Available field types and their actual class:

 - *checkbox*: `wtforms.fields.BooleanField`
 - *decimal*: `wtforms.fields.DecimalField`
 - *date*: `wtforms.fields.DateField`
 - *datetime*: `wtforms.fields.DateTimeField`
 - *float*: `wtforms.fields.FloatField`
 - *int*: `wtforms.fields.IntegerField`
 - *radio*: `wtforms.fields.RadioField`
 - *select*: `wtforms.fields.SelectField`
 - *selectmulti*: `wtforms.fields.SelectMultipleField`
 - *text*: `wtforms.fields.StringField`
 - *textarea*: `wtforms.fields.TextAreaField`
 - *password*: `wtforms.fields.PasswordField`
 - *upload*: `wtforms.fields.FileField`
 - *hidden*: `wtforms.fields.HiddenField`
 - *date5*: `wtforms.fields.html5.DateField`
 - *datetime5*: `wtforms.fields.html5.DateTimeField`
 - *datetimelocal*: `wtforms.fields.html5.DateTimeLocalField`
 - *decimal5*: `wtforms.fields.html5.DecimalField`
 - *decimalrange*: `wtforms.fields.html5.DecimalRangeField`
 - *email*: `wtforms.fields.html5.EmailField`
 - *int5*: `wtforms.fields.html5.IntegerField`
 - *intrange*: `wtforms.fields.html5.IntegerRangeField`
 - *search*: `wtforms.fields.html5.SearchField`
 - *tel*: `wtforms.fields.html5.TelField`
 - *url*: `wtforms.fields.html5.URLField`

## Defining reusable forms

You can define reusable forms using template by creating html files in the *forms* folder
at the root of your project. These files are standard templates in which you can define
you forms as described in the previous section. The form instance will always be available
as the *form* variable.

You can then use these forms with the *form* action by referencing their name (ie. the filename
without the .html extension). Finally, you can invoke the form instance like a function to
render the template.

For example, let's define *forms/SignupForm.html*:

    <{ form_tag form=form }>
        <{ form_field field=form.firstname.text() }/>
        <{ form_field field=form.lastname.text() }/>
        <{ form_field field=form.email.email() }/>
        <{ form_field field=form.password.password() }/>
        <{ form_btn }/>
    </{ form_tag }>

Then in a view:

    ---
    url: /signup
    actions:
      - form: SignupForm
    ---
    {{ form() }}

Keyword arguments used when calling `form()` will be available as variables in the form template.

## Defining forms programmatically

You can create form classes programmatically by subclassing `frasco_forms.form.Form`
and then registering them by calling `register(form_class)` on the feature:

    from frasco_forms import Form, fields

    class SignupForm(Form):
        firstname = fields.text()
        lastname = fields.text()
        email = fields.email()
        password = fields.password()

    # ...

    app.features.forms.register(SignupForm)

Then you can use the *form* action with the template name *SignupForm*:

    ---
    url: /
    actions:
      - form: SignupForm
    ---

`fields` is just an object which provide a quick way to initialize field classes.
For example, `fields.text` directly maps to `wtforms.fields.StringField` and takes the same
arguments as the latter.


## Template macros

### form\_tag

Prints the `<form>` tag and hidden fields (including the csrf token).

    <{ form_tag form=form }>
        {{ form.firstname.text() }}
    </{ form_tag }>

### form\_field

Wraps a field inside a paragraph and prints the label before the field
(unless if it's a checkbox). Also prints a span element with an error
class containing error messages and a span element with a description class
and the field's description when applicable.

    <{ form_tag form=form }>
        <{ form_field field=form.firstname.text() }/>
    </{ form_tag }>

### form\_btn

Print a submit button wrapped in a paragraph with the button class.
The default label is "Submit" and it can be overrided with the *label* option.

    <{ form_tag form=form }>
        <{ form_field field=form.firstname.text() }/>
        <{ form_btn }/>
    </{ form_tag }>

## Uploading files

Frasco-Forms makes it really easy to upload files. The way uploaded files are
stored can be changed using custom backends but only the *local* backend is included.
It stores files in the folder defined by the *upload_dir* option.

To upload a file, you'll need to use the *upload* field in your form. When the
form is submitted, the value of the field will be a safe filename which is generated
according to the rules defined in the options.

Note: when using the *local* backend, the filename is relative to the upload folder.

The upload field can take a *allowed_exts* parameter with a list of allowed file
extensions.

To get the url associated to uploaded files, you can use `url_for_upload` which is
a template global (or importable using `from frasco_forms import url_for_upload`).
It takes as parameter the filename as returned by the upload field.

Example, uploading a file and storing the filename using a model from Frasco-Models:

    ---
    url: /upload
    actions:
      - form
    actions.form_submitted:
      - save_form_model: Image
    ---
    <{ form_tag form=form }>
        <{ form_field field=form.filename.upload(required=True, allowed_exts=["jpg", "png"]) }/>
        <{ form_btn }/>
    </{ form_tag }>

Referencing the uploaded file:

    ---
    url: /images
    actions:
      - find_models: Image
    ---
    {% for img in images %}
        <img src="{{ url_for_upload(img.filename) }}" alt="">
    {% endfor %}

## Creating a custom upload backend

Upload backends are classes which must implement two methods:

 - `save(file, filename)`: will be called to save the file. The first argument
   is a file object (from Flask's `request.files`) and the second the filename
   generated by the upload field
 - `url_for(filename)`: must return the url from which the file referenced by
   the filename is accessible

To register your backend, apply the `file_upload_backend` decorator on your class with a short
name as only argument.

    from frasco_forms import file_upload_backend

    @file_upload_backend("my_backend")
    class MyBackend(object):
        def save(self, file, filename):
            pass

        def url_for(self, filename):
            pass

## Signals

 - *form_validation_failed*:
   - *form*: the form instance
 - *form_submitted*:
   - *form*: the form instance
 - *form_created_from_view*:
   - *view*: the view instance
   - *form_class*: the form class