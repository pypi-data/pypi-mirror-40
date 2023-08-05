(function($) {

  // http://ckeditor.com/forums/CKEditor/Inline-config-not-loading
  if (CKEDITOR.env.ie && CKEDITOR.env.version < 9) {
    CKEDITOR.tools.enableHtml5Elements(document);
  }

  $.fn.emailhubEditor = function(opts) {

    // Default settings
    var settings = $.extend({
      elements: {
        bodyHtml: '#emailhub-emailmessage-body-html',
        bodyText: '#emailhub-emailmessage-body-text',
        buttons: {
          remove: '#emailhub-emailmessage-remove',
          save: '#emailhub-emailmessage-save',
          send: '#emailhub-emailmessage-send'
        }
      },
      colors: {
        unchanged: '#ffffff',
        changed: '#ffdca8'
      },
      editorConfig: {
        language: 'en',
        width: 'auto',
        height: 500,
        toolbarGroups: [
          { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
          { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
          { name: 'editing', groups: [ 'find', 'selection', 'spellchecker', 'editing' ] },
          { name: 'forms', groups: [ 'forms' ] },
          { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
          { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
          { name: 'links', groups: [ 'links' ] },
          { name: 'insert', groups: [ 'insert' ] },
          { name: 'styles', groups: [ 'styles' ] },
          { name: 'colors', groups: [ 'colors' ] },
          { name: 'tools', groups: [ 'tools' ] },
          { name: 'others', groups: [ 'others' ] }
        ],
        removeButtons:
          'About,ShowBlocks,BGColor,Styles,Font,FontSize,Flash,PageBreak,Iframe,'+
          'Anchor,Language,Blockquote,CreateDiv,CopyFormatting,Superscript,'+
          'Subscript,Strike,Underline,Form,Checkbox,Radio,TextField,Select,Button,'+
          'HiddenField,Scayt,Save,NewPage,Preview,Print,Format,TextColor,Outdent,Indent'
      },
      messages: {
        html_changed_confirm: 'The HTML version has changed, but not the text version. Are you sure you want to save this message ?',
        text_changed_confirm: 'The text version has changed, but not the HTML version. Are you sure you want to save this message ?'
      }
    }, opts);

    var state = {
      hasChanged: false,
      textHasChanged: false,
      htmlHasChanged: false,
      originalHTML: '',
      originalTEXT: '',
      editorText: null,
      editorHTML: null
    };

    var ui = {
      buttons: {
        remove: $(settings.elements.buttons.remove),
        save: $(settings.elements.buttons.save),
        send: $(settings.elements.buttons.send)
      }
    };

    var on_message_modified = function(e) {
      state.hasChanged = true;
      $('.message-modified').removeClass('hide');
      ui.buttons.save.removeClass('disabled');
      ui.buttons.send.addClass('disabled');
      if (state.textHasChanged) {
        $('.messaging-tabs .text').addClass('modified');
        state.editorText.css('border-color', settings.colors.changed);
      }
      else {
        state.editorText.css('border-color', settings.colors.unchanged);
      }
      if (state.htmlHasChanged) {
        $('.messaging-tabs .html').addClass('modified');
        state.editorHTML.setUiColor(settings.colors.changed);
      }
      else {
        state.editorHTML.setUiColor(settings.colors.unchanged);
      }
    }

    var on_message_saved = function(e) {
      state.hasChanged = false;
      state.textHasChanged = false;
      state.htmlHasChanged = false;
      state.editorHTML.setUiColor(settings.colors.unchanged);
      $('.message-modified').addClass('hide');
      ui.buttons.send.removeClass('disabled');
      ui.buttons.save.addClass('disabled');
      $('.messaging-tabs .text, .messaging-tabs .html').removeClass('modified');
    }

    var on_message_save = function(e) {
      e.preventDefault();
      var url = $(this).attr('href');
      var do_save = true;
      if (state.hasChanged) {
        if (state.textHasChanged && !state.htmlHasChanged) {
          do_save = confirm(settings.messages.text_changed_confirm);
        }
        else if (!state.textHasChanged && state.htmlHasChanged) {
          do_save = confirm(settings.messages.html_changed_confirm);
        }
      }
      if (do_save) {
        var data = {
          text_content: state.editorText.val(),
          html_content: state.editorHTML.getData()
        };
        $.post(url, data)
          .done(function(response) {
            if (response.success) {
              console.log([{content: response.message, css_class: 'alert-success'}])
              on_message_saved();
            }
            else {
              alert(settings.messages.save_error)
              console.error(response);
            }
          })
        .fail(function(response) {
          alert(settings.messages.save_error)
          console.error(response);
        });
      }
      return false;
    };

    var initialize = function(){
      state.editorText = $(settings.elements.bodyText);
      state.editorHTML = CKEDITOR.replace($(settings.elements.bodyHtml).attr('id'), settings.editorConfig);
      state.originalHTML = state.editorHTML.getData(),
      state.originalTEXT = state.editorText.val()

      ui.buttons.save.bind('click', on_message_save);
      state.editorHTML.on('change', function(e){
        if (!state.htmlHasChanged) {
          var data = state.editorHTML.getData();
          if (state.originalHTML != data) {
            state.htmlHasChanged = true;
            on_message_modified();
          }
        }
      });

      state.editorText.on('keyup', function(e){
        if (!state.textHasChanged) {
          var data = state.editorText.val();
          if (state.originalTEXT != data) {
            state.textHasChanged = true;
            on_message_modified();
          }
        }
      });
    }

    return this.each(initialize);

  }; // $.fn.emailhubEditor

}(jQuery));
