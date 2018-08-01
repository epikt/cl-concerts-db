function flash(message,category){
   if (category == 'error'){
      var icon='icon-exclamation-sign';
      category='danger';
      }
   else if (category == 'success')
      var icon='icon-ok-sign';
   else
      var icon='icon-info-sign';    

   $("#message_flasher")[0].innerHTML = ""

   $('<div class="alert alert-'+category+'"><i class="'+icon+'"></i>&nbsp;<a class="close" data-dismiss="alert">×</a>'+ message +'</div>').prependTo('#message_flasher').hide().slideDown('slow');
   $.smoothScroll({
     scrollElement: $('body'),
     scrollTarget: '#main_header'
   });
}