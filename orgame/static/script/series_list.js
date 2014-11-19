$(document).ready(function(){
  var episode_list_cache = {}
  episode_list_cache['test'] = 1;
  $('.series_box').click(function(){
    series_id = $(this).data('id');
    if (episode_list_cache[series_id])
      set_episode_list(episode_list_cache[series_id]);
    else {
      $.ajax({
        type: "POST",
        url: '/series/',
        data: {series_id:series_id},
        success: function(data){
          if (data.error)
            sweetAlert('아니?! 무슨 짓이오',data.message,'error');
          else{
            episode_list_cache[series_id] = data.series_episodes;
            set_episode_list(data.series_episodes);
          }
        }
      });
    }
  });
});

function set_episode_list(episodes){
  episode_list = $('#episode_list');
  episode_list.empty();
  for (var episode in episodes){
    episode = episodes[episode];
    episode_list.append("<li data-id="+episode.id+">"+episode.name+"</li>");
  }
}


