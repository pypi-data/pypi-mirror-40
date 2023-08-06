(function($){
  'use strict';
  $(document).ready(function() {
    $('.objects').on('click', '.js-wagtailcloudinary', function(e){
      e.preventDefault();
      var link = $(this);
      var id = link.data('target')
      ModalWorkflow({
        url: link.data('url'),
        responses: {
          imageChosen: function(imageData) {
            var preview_id = '#preview_' + id;
            var input = $('#'+id);
            var preview = $('#preview_' + id);

            input.val(imageData.value);
            var chooser = link.closest('.image-chooser');
            if (imageData.url != ''){
              preview.attr({src: imageData.url})
              chooser.removeClass('blank');
            } else {
              chooser.addClass('blank');
              preview.attr({src: 'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw'})
            }
          }
        },
        onload: {
          'chooser':  function(modal){
            function ajaxifyLinks (context) {
              $('.listing a.image-choice', context).click(function() {
                modal.loadUrl(this.href);
                return false;
              });
              $('.wagtailcloudinary-tag-wrapper a').click(function(e){
                e.preventDefault();
                $(this).parent().remove();
              })

              $('.js-wagtailcloudinary-update-tags').click(function(e){
                e.preventDefault();
                $('.wagtailcloudinary-overlay', $(this).closest('.wagtailcloudinary-item')).fadeIn();
              });

              $('.js-wagtailcloudinary-update').click(function(e){
                e.preventDefault();
                var link = $(this);
                var overlay = link.closest('.wagtailcloudinary-overlay');
                var oldtags = $('input[type="hidden"]', overlay).val();
                var addedtags = $('input[type="text"]', overlay).val().split(',');
                var newtags = []
                $('.wagtailcloudinary-tags-holder .tag', overlay).each(function(){
                  newtags.push($(this).text());
                });
                for (var item in addedtags){
                  newtags.push(addedtags[item].trim());
                }
                newtags = newtags.join(',');
                if (newtags != oldtags) {
                  $.post(link.data('ajax-url'), {'tags': newtags})
                    .done(function(data){
                      link.closest('.wagtailcloudinary-overlay').fadeOut();
                      link.closest('.wagtailcloudinary-item').html(data.html);
                      ajaxifyLinks();
                      return;
                    });
                }
                link.closest('.wagtailcloudinary-overlay').fadeOut();
              });
              $('.js-wagtailcloudinary-update-cancel').click(function(e){
                e.preventDefault();
                $(this).closest('.wagtailcloudinary-overlay').fadeOut();
              });
            }

            ajaxifyLinks(modal.body);

            function init_loadmore(){
              $('.js-wagtailcloudinary-more').off('click');
              $('.js-wagtailcloudinary-more').on('click', function(e){
                e.preventDefault();
                var link = $(this);
                $.get(link.data('ajax-url'), {'next': link.data('next'), 'tag': link.data('tag')})
                  .done(function(data) {
                    $('.wagtailcloudinary-wrapper .listing').append(data.html);
                    if (data.next){
                      link.show();
                      link.data('next', data.next);
                    } else {
                      link.hide();
                    }
                    ajaxifyLinks(modal.body);
                  });
              });
            }
            function init_tags(){
              $('.js-wagtailcloudinary-tag').off('click');
              $('.js-wagtailcloudinary-tag').on('click', function(e){
                e.preventDefault();
                var link = $(this);
                var tag = link.data('tag');
                var tags = $('.tags');
                var tagclass = '.tag-__all__';
                if (tag)
                  tagclass = '.tag-'+decodeURIComponent(tag);
                $('.status-tag', tags).removeClass('icon icon-view');
                $('.status-tag'+tagclass, tags).addClass('icon icon-view');
                $.get(link.attr('href'), {'tag': tag})
                  .done(function(data) {
                    $('.wagtailcloudinary-wrapper .listing').html(data.html);
                    if (data.next){
                      $('.js-wagtailcloudinary-more').show();
                      $('.js-wagtailcloudinary-more').data('next', data.next);
                      $('.js-wagtailcloudinary-more').data('tag', tag);
                    } else {
                      $('.js-wagtailcloudinary-more').hide();
                    }
                    ajaxifyLinks(modal.body);
                  });
              });
            }

            init_loadmore();
            init_tags();

            var jqXHR = {};

            $(document).bind('drop dragover', function (e) {
              e.preventDefault();
            });

            $(document).on('dragover', '.drop-zone', function(e){
              $(this).addClass('hovered');
            });
            $(document).on('dragleave', '.drop-zone', function(e){
              $(this).removeClass('hovered');
            });
            $(document).on('drop', '.drop-zone', function(e){
              $(this).removeClass('hovered');
            });
            // $(document).on('click', '.cancel-upload', function(){
            //   var image_type = $(this).data('target');
            //   jqXHR[image_type].abort();
            //   $('.cancel-upload').addClass('is-hidden');
            //   $('.progress').addClass('is-hidden');
            //   $('.progress .bar').css({width: '0%'});
            //   return false;
            // });
            function init_fileupload(obj){
              obj.fileupload({
                dataType: 'json',
                dropZone: $('.drop-zone'),
                pasteZone: null,
                done: function (e, data) {
                  $.each(data.result.images, function (index, image) {
                    $('.wagtailcloudinary-upload-wrapper .listing').append(image.html);
                    ajaxifyLinks(modal.body);
                    $('.progress .bar').css({width: '0%'});
                    $('.progress').removeClass('active');
                    // $('.cancel-upload').addClass('is-hidden');
                  });
                },
                progress: function (e, data) {
                  var progress = parseInt(data.loaded / data.total * 100, 10);
                  $('.progress .bar').css('width', progress+'%');
                },
                add: function (e, data) {
                  // $('.cancel-upload').removeClass('is-hidden');
                  $('.progress').addClass('active');
                  jqXHR[$(this).attr('name')] = data.submit();
                }
              });
            }
            $('.fileupload').each(function(){
              init_fileupload($(this));
            });
          },
          'select': function(modal, json_data) {
            modal.respond('imageChosen', json_data.image_json); // {{ image_json|safe }});
            modal.close();
          }




        }
      });
    });
    $('.objects').on('click', '.js-wagtailcloudinary-clear', function(e){
      e.preventDefault();
      var link = $(this);
      link.closest('.image-chooser').addClass('blank');
      $('#'+link.data('target')).val('');
      $('#preview_'+link.data('target')).attr('src', 'data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw');
    });
  });
})(jQuery);
