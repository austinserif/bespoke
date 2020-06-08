$(async function() {

    /** ---------------- EVENT LISTENERS ------------------- */

    $searchButton = $(".search-button");
    $searchField = $(".search-field");
    $searchForm = $(".search-form");

    /** search term if entry is valid with search button click */
    $searchButton.on("click", async function(evt) {      
        if ($searchField.val().length > 0) {
            await getSearchResults($searchField.val());
        }
        $searchField.val("");
    });

    /** search term if entry is valid with form submit */
    $searchForm.on("submit", async function(evt) {
        evt.preventDefault();
        if ($searchField.val().length > 0) {
            await getSearchResults($searchField.val());
        }
        $searchField.val("");
    });

    /** listen for click/tap on tagged keywords, get related articles from server, and post to DOM*/
    $(".mdl-chip.mdl-chip--deletable.tag").on("click tap", async function(evt) {
        let tag_id = this.id;
        const response = await getArticles(tag_id);
        await addNewTagResults(response.data.articles, response.data.tag_name);
    });

    /** event listener for adding tag from search history */
    $(`.mdl-chip__contact.search`).on("click", async function(evt) {
        let item_id = $(this).data("id");
        console.log(item_id);
        const response = await addTagOnServer(item_id);
        if (response.data.result) {
            await addNewTag(response.data.tag_id, response.data.tag_name);
            await showTagBannerSuccess(response.data.tag_name);
        } else {
            showTagAlreadyExistsBanner();
        }
    });

    /** listen for click on a tag's cancel button, remove from DOM 
     * and tell server to update display property to False */
    $("button.tag").on("click", async function(evt) {
        let tag_id = $(this).data("id");
        $(`#${tag_id}.tag`).remove();
        await deleteTaggedItem(tag_id);
    });

    /** listen for click on a search item's cancel button, remove from DOM 
     * and tell server to update display property to False */
    $("button.search").on("click", async function(evt) {
        let item_id = $(this).data("id");
        $(`#${item_id}.search`).remove();
        await deleteSearchedItem(item_id);
    });

    /** pass in valid search term and return array of results, update db to 
     * reflect new search history on the server side */
    async function getSearchResults(term) {
        const response = await axios.get(`/search?term=${term}`)
        await showSearchResults(response.data.articles);
        const item_id = response.data.item_id;
        addSearchedItem(term, item_id);
    }




    /** ---------------- SEARCH ITEMS ------------------- */




    /** add new item to search history on the DOM, add new event listeners to each*/
    function addSearchedItem(term, item_id) {
        $("#dash-searches-cell").prepend(
            `<span id="${item_id}" class="mdl-chip mdl-chip--deletable search">
                <span class="mdl-chip__contact mdl-color--teal mdl-color-text--white material-icons ${item_id}-search search" style="transform: translateX(-12px);" data-id="${item_id}">add</span>
                
                <span class="mdl-chip__text ${item_id}-search search">${term}</span>
                <button type="button" class="mdl-chip__action ${item_id}-search search" data-id="${item_id}">
                    <i class="material-icons ${item_id}-search search">cancel</i>
                </button>
            </span>`);

        $(`button.${item_id}-search`).on("click", async function(evt) {
            $(`#${item_id}.search`).remove();
            await deleteSearchedItem(item_id);
        });

        /** event listener for adding tag from search history */
        $(`.mdl-chip__contact.${item_id}-search`).on("click", async function(evt) {
            const response = await addTagOnServer(item_id);
            if (response.data.result) {
                await addNewTag(response.data.tag_id, response.data.tag_name);
                await showTagBannerSuccess(term);
            } else {
                showTagAlreadyExistsBanner();
            }
        });
    }



    /** ---------------- HTTP REQUESTS ------------------- */




    /** make request to server with tag_id, return server's response */
    async function getArticles(tag_id) {
        const response = await axios({
            method: 'get',
            url: `tag/articles?tag_id=${tag_id}`
        });
        return response;
    }

    /** make post request to server with item_id of search history item (in order to register it as a tag), 
     * return response from server  */
    async function addTagOnServer(item_id) {
        const response = await axios({
            method: 'post',
            url: '/tag/add',
            data: {item_id}
        });
        return response;
    }

    /** tell the server to set display property of a given search_item to false */
    async function deleteSearchedItem(item_id) {
        await axios({
            method: 'post',
            url: '/search/delete',
            data: {item_id}
        });
    }

    /** tell server side to change display column to False on associated tag */
    async function deleteTaggedItem(tag_id) {
        await axios({
            method: 'post',
            url: '/tag/delete',
            data: {tag_id}
        });
    }


    

    /** ---------------- DOM MANIPULATORS ------------------- */




    /** pass in a list of articles and append them to search results page on the DOM */
    async function showSearchResults(results) {
        for (item of results) {
           $("#dash-search-results-cell").prepend(
                `<div class="card mdl-cell">
                    <img class="card-img-top" src=${item.urlToImage} alt="Card image cap">
                    <div class="card-body">
                        <h5 class="card-title">${item.title}</h5>
                        <p class="card-text">${item.description}</p>
                        <a href="${item.url}" class="mdl-button mdl-js-button mdl-js-ripple-effect" style="text-decoration: none;">Go To ${item.source.name}</a>
                    </div>
                </div>`
            );
        }
    }

    /** add new tag to the DOM given a tag_id and name, attach event listeners to tag*/
    async function addNewTag(id, name) {
        $("#active-tags").prepend(`
        <span id="${id}" class="mdl-chip mdl-chip--deletable tag">
        <span class="mdl-chip__text ${id}-tag tag">${name}</span>
        <button type="button" class="mdl-chip__action ${id}-tag tag" data-id="${id}">
            <i class="material-icons ${id}-tag tag">cancel</i>
        </button>
        </span>
        `);

        /** when tag cancel button is selected, remove from DOM and tell server to change display */
        $(`.mdl-chip__action.${id}-tag`).on("click", async function(evt) {
            $(`#${id}.tag`).remove();
            await deleteTaggedItem(id);
        });

        /** when tag body is selected, display articles related to tag's keyword */
        $(`#${id}.mdl-chip.mdl-chip--deletable`).on("click tap", async function(evt) {
            let tag_id = id;
            const response = await getArticles(tag_id);
            await addNewTagResults(response.data.articles, response.data.tag_name);
        });
    }

    /** add articles to DOM associated with newly added tag item*/
    async function addNewTagResults(results, tag_name) {
        for (item of results) {
            $("#feed").prepend(
                `<div class="card mdl-cell">
                    <img class="card-img-top" src=${item.urlToImage} alt="Card image cap">
                    <div class="card-body">
                        <h5 class="card-title">${item.title}</h5>
                        <p class="card-text">${item.description}</p>
                        <a href="${item.url}" class="mdl-button mdl-js-button mdl-js-ripple-effect" style="text-decoration: none;">Go To ${item.source.name}</a>
                        <span class="mdl-chip" style="background-color: red;">
                            <span class="mdl-chip__text">${tag_name}</span>
                        </span>
                    </div>
                </div>`
            );
        }
    }

    /** remove any current banners and add a new "tag failed" banner to DOM for 
     * the added tag with instructions on how to view */
    function showTagAlreadyExistsBanner() {
        $("#search-banner").empty();
        $("#search-banner").html(`<div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>You've already tagged this term!</strong> No need to add this term again. To find it just head over to the home feed by clicking <span class="material-icons">home</span>.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>`)
    }
    
    /** remove any current banners and add a new success banner to DOM for 
     * the added tag with instructions on how to view */
    async function showTagBannerSuccess(term) {
        $("#search-banner").empty();
        $("#search-banner").html(`<div class="alert alert-success alert-dismissible fade show" role="alert">
        <strong>Tag Added!</strong> You've started tracking a new tag! You can find articles related to "${term}" in your home feed. Just click <span class="material-icons">home</span>.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>`)
    }
});