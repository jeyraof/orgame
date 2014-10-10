from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from series.models import Series, Episode


class SeriesView(View):
    template_path = 'series/series.html'

    def get(self, request, series_id=None):
        opt = {}
        if series_id:
            opt['is_new'] = False
            opt['series'] = get_object_or_404(Series, id=series_id)
            opt['episode_list'] = Episode.objects.filter(series_id=series_id).order_by('episode').all()

        else:
            opt['is_new'] = True

        return render(request, self.template_path, opt)

    def post(self, request):
        data = request.POST

        series_name = data.get('series_name', None)
        if series_name:
            series = Series.objects.create(category=None, name=series_name)
            series.save()
            return redirect('series', series_id=series.id)

        else:
            return redirect('series_new')


class EpisodeView(View):

    def get(self, request, series_id=None, episode_id=None):
        opt = {}
        try:
            opt['series'] = Series.objects.get(id=series_id)
        except Series.DoesNotExist:
            return redirect('main')

        try:
            opt['episode'] = Episode.objects.get(id=episode_id)
        except Episode.DoesNotExist:
            return redirect('series', series_id=series_id)

        return render(request, 'series/episode.html', opt)



    def post(self, request, series_id=None):
        data = request.POST
        try:
            series = Series.objects.get(id=series_id)
        except Series.DoesNotExist:
            return redirect('main')

        episode_number = data.get('episode_number', '')
        if not episode_number.isdigit():
            return redirect('series', series_id=series_id)

        episode_name = data.get('episode_name', '')

        episode = Episode.objects.create(series=series, episode=episode_number, name=episode_name)
        episode.save()
        return redirect('series', series_id=series_id)