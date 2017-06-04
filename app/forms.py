# -*- encoding: utf-8 -*-

#from flask_wtf import Form       ### flask_wtf instead of flask.ext.wtf
from flask_wtf      import FlaskForm ### FlaskWTFDeprecationWarning: "flask_wtf.Form" has been renamed to "FlaskForm" and will be removed in 1.0.
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import validators

### import field classes
from wtforms import StringField, BooleanField, TextAreaField, IntegerField, PasswordField, SubmitField, HiddenField, widgets #, Form
from wtforms.fields.html5 import URLField, EmailField
from wtforms.fields.core import SelectField, SelectMultipleField, RadioField, DateTimeField, DateField

from wtforms.validators import DataRequired, Length, EqualTo, URL, Email, Optional


from scripts.app_db_settings import * #dict_db_user, dict_user_db


#ALLOWED_EXTENSIONS     = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#ALLOWED_IMAGES         = ['png', 'jpg', 'jpeg', 'gif']

HTMLclass_form_control  = 'form-control'
HTMLclass_checkbox_line = 'checkbox-inline'
HTMLclass_radio_line    = 'radio-inline'
HTMLclass_btn_danger    = 'btn btn-danger'

'''
choices_state           = [ ("na", "na"), ("project", "project"), ("in development","in development"), ("in stand by","in stand by"), ("finished","finished") ]
choices_type            = [ ("article", "article"), ("category","category"), ("project", "project"), ("reference", "reference") ]
choices_state.sort( key=lambda art : art[0].lower() )
choices_type.sort( key=lambda art : art[0].lower() )
'''


### forms classes/typologies

class LoginForm(FlaskForm):
    userName     = StringField   ( 'user name'    , validators = [ Optional() ],     render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_username] }  )
    userCard     = IntegerField  ( 'user card'    , validators = [ Optional() ],     render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_n_carte]  }  )
    userPassword = PasswordField ( 'user password', validators = [ DataRequired() ], render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_password] }  )
    #remember_me  = BooleanField  ( 'remember_me', default=False )

class UserRegisterForm(FlaskForm):
    userName        = StringField   ( 'user name'    , validators = [ DataRequired(), Length(min=3, max=50) ], render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_username] }  )
    userCard        = IntegerField   ( 'user card'    , validators = [ Optional() ],                            render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_n_carte]  }  )
    userEmail       = EmailField    ( 'user email'   , validators = [ DataRequired(), Length(min=7, max=50) ], render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_email]    }  )
    userPassword    = PasswordField ( 'user password',
        [
        DataRequired(),
        EqualTo('confirmPassword', message=u'les deux mots de passe doivent être identiques'),
        Length(min=4, max=100)
        ],
        render_kw={'class': HTMLclass_form_control, 'placeholder': u'votre ' + dict_db_user[key_password] }
    )
    confirmPassword = PasswordField ('repeat Password', render_kw={'class': HTMLclass_form_control, 'placeholder':u'répéter votre ' + dict_db_user[key_password] } )
    #remember_me     = BooleanField  ( 'remember_me', default=False )

class UserUpdateForm(FlaskForm):
    new_userName        = StringField   ( 'user name'    , validators = [ DataRequired(), Length(min=3, max=50) ], render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre nouveau ' + dict_db_user[key_username] }  )
    new_userCard        = StringField   ( 'user card'    , validators = [ DataRequired() ],                        render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre nouveau ' + dict_db_user[key_n_carte]  }  )
    new_userEmail       = EmailField    ( 'user email'   , validators = [ Optional(), Length(min=7, max=50) ],     render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre nouveau ' + dict_db_user[key_email]    }  )
    new_userPassword    = PasswordField ( 'user password',
        [
        Optional(),
        EqualTo('confirmPassword', message=u'les deux champs "mot de passe" doivent être identiques'),
        Length(min=4, max=100)
        ],
        render_kw={'class': HTMLclass_form_control, 'placeholder': u'votre nouveau ' + dict_db_user[key_password] + u" (optionnel)"}
    )
    confirmPassword = PasswordField ('repeat Password', render_kw={'class': HTMLclass_form_control, 'placeholder':u'répéter votre nouveau ' + dict_db_user[key_password] } )
    #remember_me     = BooleanField  ( 'remember_me', default=False )

class UserHistoryAloesForm(FlaskForm):
    cardPassword = PasswordField ( 'user password', validators = [ DataRequired() ], render_kw={'class': HTMLclass_form_control, 'placeholder':u'votre ' + dict_db_user[key_password] + u" de carte de bibliothèque"}  )

class RequestCabForm(FlaskForm):
    cab_code     = IntegerField  ( u'barcode',       validators = [ DataRequired() ],       render_kw={'class': HTMLclass_form_control, 'placeholder':u"le code barre de l'ouvrage ", "onfocus":u"this.placeholder = ''"}  )
    categ        = RadioField    ( u'catégorie',     choices=[ (u'envie',u'envie de lire'),(u'val2',u'ouvrage lu') ], render_kw={'class': HTMLclass_radio_line}, default=u'envie' )


'''
class MultipleCheckboxField(SelectMultipleField):
    widget        = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CheckboxField(SelectField):
    widget        = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ArticleForm(FlaskForm):

    art_id               = HiddenField   ( 'art_id' )

    art_title            = StringField   ( 'title'          , validators = [ DataRequired(), Length(min=2, max=50 ) ], render_kw={'class': HTMLclass_form_control} )

    art_period           = StringField   ( 'period'         , render_kw={'class': HTMLclass_form_control} )
    art_place            = StringField   ( 'place'          , render_kw={'class': HTMLclass_form_control} )

    art_tooltip          = StringField   ( 'tooltip'        , validators = [ DataRequired(), Length(min=4, max=200) ], render_kw={'class': HTMLclass_form_control} )
    art_abstract         = TextAreaField ( 'abstract'       , validators = [ DataRequired(), Length(min=4, max=1500) ], render_kw={'class': HTMLclass_form_control } )

    art_type             = RadioField    ( 'types'          ,
                                          validators = [ DataRequired() ],
                                          coerce = str,
                                          choices = choices_type,
                                          render_kw={'class': HTMLclass_radio_line } )

    art_state            = RadioField    ( 'states',
                                          validators = [ DataRequired() ],
                                          coerce = str,
                                          choices = choices_state,
                                          render_kw={'class': HTMLclass_radio_line } )

    #art_connections      = SelectMultipleField ( 'boxes', coerce = str, choices = [] )

    art_connections_cat  = MultipleCheckboxField ( 'boxes',
                                                  #validators = [ DataRequired() ],
                                                  coerce = str,
                                                  choices = [],
                                                  render_kw={'class': HTMLclass_checkbox_line } )

    art_connections_art  = MultipleCheckboxField ( 'boxes',
                                                  #validators = [ DataRequired() ],
                                                  coerce = str,
                                                  choices = [],
                                                  render_kw={'class': HTMLclass_checkbox_line } )

    art_connections_pro  = MultipleCheckboxField ( 'boxes',
                                                  #validators = [ DataRequired() ],
                                                  coerce = str,
                                                  choices = [],
                                                  render_kw={'class': HTMLclass_checkbox_line } )
    art_connections_ref  = MultipleCheckboxField ( 'boxes',
                                                  #validators = [ DataRequired() ],
                                                  coerce = str,
                                                  choices = [],
                                                  render_kw={'class': HTMLclass_checkbox_line } )

    art_tags             = StringField   ( 'tags'           , render_kw={'class': HTMLclass_form_control} )

    art_icon_file        = FileField     ( 'icon file'      , validators = [ FileAllowed(ALLOWED_IMAGES, 'Images only!' ) ], render_kw={} )
    art_icon_filename    = HiddenField   ( 'icon_filename' )
    art_cover_file       = FileField     ( 'cover file'     , validators = [ FileAllowed(ALLOWED_IMAGES, 'Images only!' ) ], render_kw={} )
    art_cover_filename   = HiddenField   ( 'cover_filename' )
    art_images_files     = FileField     ( 'images files'   , validators = [ FileAllowed(ALLOWED_IMAGES, 'Images only!' ) ] , render_kw={'multiple': True} )
    art_images_filenames = HiddenField   ( 'images_filenames' )

    art_links            = URLField      ( 'links'          , render_kw={'class': HTMLclass_form_control} )

    #submit               = SubmitField   ("Save")


class DeleteForm(FlaskForm):

    doc_type             = HiddenField   ( 'doc_type' )
    art_id               = HiddenField   ( 'art_id' )
    choices              = [ ("yes", "yes"), ("no","no") ]
    confirmation         = RadioField    ( 'Confirmation'          ,
                                          validators = [ DataRequired() ],
                                          coerce = str,
                                          choices = choices,
                                          render_kw={'class': HTMLclass_radio_line } )
    submit_delete        = SubmitField("delete", render_kw={'class': HTMLclass_btn_danger })


class CommentForm (FlaskForm):

    art_id   = HiddenField   ( 'art_id' )
    com_con  = HiddenField   ( 'com_con' )
    com_user = HiddenField   ( 'com_user' )
    com_text = TextAreaField ( 'comment' , validators = [ DataRequired(), Length(min=3, max=140) ], render_kw={'class': HTMLclass_form_control } )
'''
