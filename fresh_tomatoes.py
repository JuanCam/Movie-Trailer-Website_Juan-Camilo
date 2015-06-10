import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Juan's movie trailer web-site</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            if(event.target.className.indexOf('move-video-modal')==-1)
                $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile,.move-video-modal', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id'),
                trailerPrev = '',
                trailerAnt = '';
            $('.movie-tile').each(function(key,value){
              if(trailerYouTubeId == value.getAttribute('data-trailer-youtube-id')){
                  //console.log($('.movie-tile').get(key - 1))
                  trailerPrev = $('.movie-tile').get(key - 1).getAttribute('data-trailer-youtube-id')
                  trailerNext = $('.movie-tile').get(key + 1).getAttribute('data-trailer-youtube-id')
              }
            })
            $(".move-video-modal.prev").attr("data-trailer-youtube-id",trailerPrev)
            $(".move-video-modal.next").attr("data-trailer-youtube-id",trailerNext)
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';

            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        //Filter by word, made by Juan Camilo Gutierrez in fresh_tomatoes file
        $(document).on( "keyup", "#text-filter" , function(){
          //Execute this piece of code when a key is released from pressing
          var value = $(this).val()
          $(".movies-container").css('display','none')
          //Get the value of the target input text and hide all the items for
          //show only the filtered items
          var filtr = $(".movies-container").filter(function(index){
              var title = $(this).find($("h2")).text().toLowerCase()//Get all items name from the h2 tag
              return title.indexOf(value) != -1//defines if the value of the input text is similar or matches the movie title
          })
          filtr.css('display','block')//Display all the filter results
          if(filtr.length <= 0){
            alert('No results found!')
          }
          //console.log(filtr)
        })

    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
          <ul class="pager">
            <li><a class="move-video-modal prev" href="#">Previous</a></li>
            <li><a class="move-video-modal next" href="#">Next</a></li>
          </ul>
        </div>
      </div>
    </div>
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Juan's movie trailer web-site</a>
          </div>
        </div>
      </div>
    </div>
<!--Added by Juan-->
    <div class="input-group col-md-offset-4 col-md-7 col-lg-4">
      <input type="text" id="text-filter" class="form-control" placeholder="Type movie's name" aria-describedby="basic-addon2">
      <span class="input-group-addon" id="basic-addon2">Movie's name <span class="glyphicon glyphicon-film"></span></span>
    </div>

    <div class="container" style="margin-top:20px">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''

  <div class="movies-container col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
      <img src="{poster_image_url}" width="220" height="342">
      <h2>{movie_title}</h2>
      <div class="panel panel-default">
        <div class="panel-heading">Storyline</div>
        <div class="panel-body">
          <div class="label label-default">Year: {year}</div>
          {storyline}
        </div>
      </div>
  </div>

'''


def create_movie_tiles_content(movies):

    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            storyline=movie.storyline,
            year=movie.year
        )
    return content


def open_movies_page(movies):

  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  # open in a new tab, if possible
  webbrowser.open('file://' + url, new=2)
