// Adds a button to hide the input part of the currently selected cells

define([
    'jquery',
    'base/js/namespace',
    'base/js/events'
], function(
    $,
    Jupyter,
    events
) {
    "use strict";
    // NOTE: all the functions should be idempotent, i.e on multiple load of same
    // function should have same behaviour
    function hide_download_options() {
        $('#download_menu > li:not(:last-child)').hide();
        $('#download_ipynb').show();
    }

    function get_git_pull_url() {
        var hub_user_url = '/hub/user-redirect';
        var repo_url = 'https://github.com/colaberry/dsin100days';
        var branch = 'master';
        var subpath = Jupyter.notebook.notebook_path.replace('dsin100days/', '');
        subpath = encodeURIComponent(subpath);
        var url = hub_user_url + '/git-pull?repo=' + repo_url + '&branch=' + branch + '&subPath=' + subpath;
        return url;
    }

    function add_update_link() {
        if($("#update_files").length == 0) {
            console.log('add update files link...');
            var url = get_git_pull_url();
            var html = '<li class="dropdown" id="update_files"><a href="#"class="dropdown-toggle" data-toggle="dropdown">Update</a>';
            // update_files link doesn't exist, so append it.
            $('.navbar-nav').append(html);
            $('#update_files').on('click', function(e) {
                window.location.href = url;
            });
        }
    }

    function load_functions() {
        hide_download_options();
        add_update_link();
    }

    var load_extension = function() {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
            load_functions();
        }
        events.on("notebook_loaded.Notebook", load_functions);
    };

    return {
        load_extension : load_extension
    };
});
