// ++++++++++++++++++++++++++++++++++++++ ON LOAD +++++++++++++++++++++++++++++++++++++++++++++

window.onload = function(){

    document.getElementById("keyword").value = "";
    document.getElementById('testform').onsubmit= function(e){
        e.preventDefault();
    }

    HomePage();

};


// ++++++++++++++++++++++++++++++++++++++ HOME ++++ +++++++++++++++++++++++++++++++++++++++++
//Populates Home page with data
function HomePage() {
        //HOME - MOVIE
        var requestObjHomeMovie = new XMLHttpRequest();
        requestObjHomeMovie.onreadystatechange = function(){
            console.log("this.readyState:"+ this.readyState);
            console.log("this.status:"+ this.status);
            if( this.readyState === 4)
            {
                if (this.status === 200)
                {
                    jsonData = requestObjHomeMovie.responseText;
                    jsonObj = JSON.parse(jsonData);
                    console.log(jsonObj);
                    movie_img = ["movie_img1", "movie_img2", "movie_img3", "movie_img4", "movie_img5"];
                    movie_name = ["movie_name1", "movie_name2", "movie_name3", "movie_name4", "movie_name5"];

                    for (var i = 0; i < jsonObj.trending_movies.length; i++) {
                        document.getElementById(movie_img[i]).src  = jsonObj.trending_movies[i].backdrop_path;
                        document.getElementById(movie_name[i]).innerText  = jsonObj.trending_movies[i].title + " (" + jsonObj.trending_movies[i].release_date.substring(0,4) + ")";
                    }

                }
            }
        }

        var URLHomeMovies = '/movies/get-trending-week';
        requestObjHomeMovie.open('GET',URLHomeMovies,true);
        requestObjHomeMovie.send();


        //HOME - TV SHOW
        var requestObjHomeTV = new XMLHttpRequest();
        requestObjHomeTV.onreadystatechange = function(){
            console.log("this.readyState:"+ this.readyState);
            console.log("this.status:"+ this.status);
            if( this.readyState === 4)
            {
                if (this.status === 200)
                {
                    jsonData = requestObjHomeTV.responseText;
                    jsonObj = JSON.parse(jsonData);
                    console.log(jsonObj);
                    TV_img = ["TV_img1", "TV_img2", "TV_img3", "TV_img4", "TV_img5"];
                    TV_name = ["TV_name1", "TV_name2", "TV_name3", "TV_name4", "TV_name5"];


                    for (var i = 0; i < jsonObj.tv_airing_today.length; i++) {
                        document.getElementById(TV_img[i]).src  = jsonObj.tv_airing_today[i].backdrop_path;
                        document.getElementById(TV_name[i]).innerText  = jsonObj.tv_airing_today[i].name + " (" + jsonObj.tv_airing_today[i].first_air_date.substring(0,4) + ")";
                    }
                }
            }
        }

        var URLHomeTV = '/tv/airing-today';
        requestObjHomeTV.open('GET',URLHomeTV,true);
        requestObjHomeTV.send();
}


// ++++++++++++++++++++++++++++++++++++++ SEARCH +++++++++++++++++++++++++++++++++++++++++++++
function click_clear(){

    document.getElementById("keyword").value = "";
    document.getElementById("categories_dropdown").selectedIndex = null;
    document.getElementById('noResults').style.display = 'none';
    document.getElementById('showingResults').style.display = 'none';
    document.getElementById('searchResults').style.display = 'none';

    var footerSearch = document.getElementById("footerSearch");
    footerSearch.style.marginTop = "480px";
}


function click_search(){

    var keyword = document.getElementById("keyword").value;
    var category = document.getElementById("categories_dropdown").value;

    var requestObjSearch = new XMLHttpRequest();
    requestObjSearch.onreadystatechange = function(){
        console.log("this.readyState:"+ this.readyState);
        console.log("this.status:"+ this.status);
        if( this.readyState === 4)
        {
            if (this.status === 200)
            {

                jsonData = requestObjSearch.responseText;
                jsonObj = JSON.parse(jsonData);
                console.log(jsonObj);

                if (jsonObj.search_results.length > 0) {
                    document.getElementById('noResults').style.display = 'none';
                    document.getElementById('showingResults').style.display = 'block';
                    document.getElementById('searchResults').style.display = 'block';

                    var searchResults = document.getElementById('searchResults');
                    //discard childnodes
                    while(document.getElementById('searchResults').hasChildNodes()) {
                        document.getElementById('searchResults').removeChild(document.getElementById('searchResults').lastChild)
                    }

                    for (var i = 0; i < jsonObj.search_results.length; i++){
                        // var title = document.createElement('p');
                        // title.innerHTML = jsonObj.search_results[i].name;
                        // searchResults.appendChild(title);

                        var result = document.createElement('div');
                        result.className = "result";

                        // part1
                        var part1_main = document.createElement('div');
                        part1_main.className = "part1-photo";

                        var img = document.createElement('img');
                        img.src = jsonObj.search_results[i].poster_path;

                        part1_main.appendChild(img);

                        // part2
                        var part2_main = document.createElement('div');
                        part2_main.className = "part2-main";
                        var heading = document.createElement("h2");
                        heading.innerText = jsonObj.search_results[i].name;
                        var year_genre = document.createElement("p");
                        year_genre.innerText = jsonObj.search_results[i].release_date.substring(0,4) + " | " + jsonObj.search_results[i].genres;
                        part2_main.appendChild(heading);
                        part2_main.appendChild(year_genre);


                        var div = document.createElement('div');
                        var span1 = document.createElement('span');
                        span1.className = "star";
                        span1.style.cssFloat = "left";
                        span1.innerHTML = "&#9733; " +  jsonObj.search_results[i].vote_average + "/5";
                        var span2 = document.createElement('span');
                        span2.className = "white";
                        span2.style.cssFloat = "left";
                        span2.style.fontSize = "12px";
                        span2.innerHTML = "&nbsp; " + jsonObj.search_results[i].vote_count + " votes" ;

                        div.appendChild(span1);
                        div.appendChild(span2);
                        part2_main.appendChild(div);

                        part2_main.appendChild(document.createElement('br'));
                        part2_main.appendChild(document.createElement('br'));

                        var overview = document.createElement("p");
                        overview.innerText = jsonObj.search_results[i].overview;
                        part2_main.appendChild(overview);


                        var showmorebutton = document.createElement("button");
                        showmorebutton.innerText = "Show more";
                        showmorebutton.id = jsonObj.search_results[i].id + "-" + jsonObj.search_results[i].media_type;
                        showmorebutton.className = "showMoreBtn";
                        showmorebutton.onclick = function(){

                            // ******************** GET DATA FOR THE POPUP ********************

                            // ******************** 1. Cast ************
                            var idValue = this.id.split("-");
                            id = idValue[0]; media_type = idValue[1];


                            var requestObjMovieDetails = new XMLHttpRequest();
                            requestObjMovieDetails.onreadystatechange = function(){
                                console.log("this.readyState:");
                                console.log("this.status:");
                                if("this.readyState" === 4);

                                    if ("this.status" === 200);

                                        jsonData = requestObjMovieDetails.responseText;
                                        p_jsonObj = JSON.parse(jsonData);
                                        console.log(p_jsonObj);

                                        document.getElementById("p_title").innerHTML = p_jsonObj.title;
                                        var info = document.createElement('a');
                                        info.target = "_blank"
                                        info.innerHTML = "&nbsp;&nbsp; &#9432; ";
                                        info.className="p_info";
                                        info.href="https://www.themoviedb.org/" + media_type + "/" + id;
                                        document.getElementById("p_title").appendChild(info);


                                        document.getElementById("p_src").src = p_jsonObj.backdrop_path;
                                        document.getElementById("p_year_genres").innerHTML = p_jsonObj.release_date.substring(0,4) + " | " + p_jsonObj.genres;
                                        document.getElementById("p_stars").innerHTML =  "&#9733; " +  p_jsonObj.vote_average + "/5 ";
                                        document.getElementById("p_votes").innerHTML = "&nbsp; " + p_jsonObj.vote_count + " votes";
                                        document.getElementById("p_overview").innerHTML = p_jsonObj.overview;
                                        document.getElementById("p_languages").innerHTML = "Spoken languages: " + p_jsonObj.spoken_languages;

                                        //CAST
                                        //////////////////////////////////////

                                        var cast_list = document.getElementById('cast_list');
                                        //discard childnodes
                                        while(document.getElementById('cast_list').hasChildNodes()) {
                                            document.getElementById('cast_list').removeChild(document.getElementById('cast_list').lastChild)
                                        }

                                        for (var j = 0; j < p_jsonObj.actors.length; j++){
                                            // var title = document.createElement('p');
                                            // title.innerHTML = jsonObj.search_results[i].name;
                                            // searchResults.appendChild(title);

                                            var modal_cast = document.createElement('div');
                                            modal_cast.className = "modal-cast";

                                            var p_img = document.createElement('img');
                                            p_img.src = p_jsonObj.actors[j].picture;
                                            modal_cast.appendChild(p_img);

                                            var gap1 = document.createElement("div");
                                            gap1.style.height = "10px";
                                            modal_cast.appendChild(gap1);


                                            var name = document.createElement("p");
                                            name.style.fontWeight = "700";
                                            name.innerHTML = p_jsonObj.actors[j].name;
                                            modal_cast.appendChild(name);
                                            var as = document.createElement("p");
                                            as.innerHTML = "AS";
                                            modal_cast.appendChild(as);
                                            var  character = document.createElement("p");
                                            character.innerHTML = p_jsonObj.actors[j].character;
                                            modal_cast.appendChild(character);

                                            var gap2 = document.createElement("div");
                                            gap2.style.height = "15px";
                                            modal_cast.appendChild(gap2);

                                            cast_list.appendChild(modal_cast);
                                        }


                                        // // ******************** 2. Reviews ************

                                        var review_list = document.getElementById('review_list');
                                        //discard childnodes
                                        while(document.getElementById('review_list').hasChildNodes()) {
                                            document.getElementById('review_list').removeChild(document.getElementById('review_list').lastChild)
                                        }

                                        for (var j = 0; j < p_jsonObj.reviews.length; j++){
                                            // var title = document.createElement('p');
                                            // title.innerHTML = jsonObj.search_results[i].name;
                                            // searchResults.appendChild(title);

                                            var modal_review = document.createElement('div');
                                            modal_review.className = "review-now";

                                            var review_username = document.createElement("h5");
                                            review_username.className = "review_heading";
                                            review_username.style.fontWeight = "700";

                                            var created_at = document.createElement('span');
                                            created_at.style.fontSize = "11px";
                                            created_at.style.fontWeight = "500";
                                            created_at.innerHTML = " on " + p_jsonObj.reviews[j].created_at ;


                                            review_username.innerHTML = p_jsonObj.reviews[j].username;
                                            review_username.appendChild(created_at);
                                            modal_review.appendChild(review_username);

                                            if (p_jsonObj.reviews[j].rating != null) {

                                            var review_stars = document.createElement('p');
                                            review_stars.className = "star";
                                            review_stars.innerHTML =  "&#9733; " +  p_jsonObj.reviews[j].rating + "/5 ";
                                            modal_review.appendChild(review_stars);
                                            }


                                            var review_content = document.createElement('div');
                                            review_content.className = "p_content";
                                            review_content.innerHTML = p_jsonObj.reviews[j].content;
                                            modal_review.appendChild(review_content);


                                            var gap3 = document.createElement("div");
                                            gap3.style.height = "10px";
                                            modal_review.appendChild(gap3);

                                            var p_reviews_separator = document.createElement('div');
                                            p_reviews_separator.className = "p_reviews_separator";
                                            modal_review.appendChild(p_reviews_separator);

                                            review_list.appendChild(modal_review);
                                        }
                                        /////////////////////////////////////


                                        //DISPLAY THE POPUP AFTER ALL DATA RECORDED
                                        modal.style.display = "block";



                                    }
                                }
                            }

                            var URLMoviesDetails = '/'+media_type+'/'+ id;
                            requestObjMovieDetails.open('GET',URLMoviesDetails,true);
                            requestObjMovieDetails.send();

                            // ******************** DISPLAY THE POPUP ********************
                            // Get the modal
                            var modal = document.getElementById("myModal");

                            // Get the <span> element that closes the modal
                            var span = document.getElementsByClassName("close")[0];

                            // When the user clicks on <span> (x), close the modal
                            span.onclick = function() {
                                modal.style.display = "none";
                            }

                            // When the user clicks anywhere outside of the modal, close it
                            window.onclicks = function(event) {
                                if (event.target == modal) {
                                modal.style.display = "none";
                                }
                            }

                          };
                        part2_main.appendChild(showmorebutton);






                        result.appendChild(part1_main);
                        result.appendChild(part2_main);
                        searchResults.appendChild(result);
                        searchResults.appendChild(document.createElement('br'));


                var footerSearch = document.getElementById("footerSearch");
                footerSearch.style.marginTop = "0px";

                    }
                }
                else {
                    //No Results
                    document.getElementById('noResults').style.display = 'block';
                    document.getElementById('showingResults').style.display = 'none';
                    document.getElementById('searchResults').style.display = 'none';

                    var footerSearch = document.getElementById("footerSearch");
                    footerSearch.style.marginTop = "378px";
                }


            }
        }
	}

    if (String(keyword) != "" && String(category) != ""){
        var url = '/search/'+ String(category) + '/' + String(keyword);
        requestObjSearch.open('GET',url,true);
        requestObjSearch.send();
    }
    else {
        alert("Please enter valid values. ");
        document.getElementById('noResults').style.display = 'none';
        document.getElementById('showingResults').style.display = 'none';
        document.getElementById('searchResults').style.display = 'none';
        var footerSearch = document.getElementById("footerSearch");
        footerSearch.style.marginTop = "480px";
    }
}