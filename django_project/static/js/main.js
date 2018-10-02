/*
#
# Author: Robert Abram <rabram991@gmail.com>
#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function system_app () {

    // Set default environment id+values here
    this.env = {

    };

    /* Store id + value pairs, p can be an array. IE: set_env({ 'id1': 'test', 'id2': 2, 'ed3': true } */
    this.set_env = function (p, value) {
        if (p != null && typeof p === 'object' && !value) for (var n in p) this.env[n] = p[n];
         else this.env[p] = value
    };


    this.unload = false;

    /* Get the csrf token */
    this.set_env({'csrftoken': Cookies.get('csrftoken') });

    $.ajaxSetup({
        cache: false,
        error: function (request, status, err) {
            /* this.http_error(request, status, err) */
        },
        beforeSend: function (xmlhttp, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xmlhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
            }
        }
    });

    /* figure out if the window is closing */
    $(window).bind('beforeunload', function () {
        this.unload = true
    });

    this.init = function () {

        /* Calculate the apply url and handle the apply button click */
        apply_url = "/" + this.env.app + "/apply/";

        $('#apply-btn').click(function () {

            $.post(apply_url, {
                type: $('#apply-type').val()
            }, function (data) {
                $('#apply-msg').html(data.message);
            }, "json")
        });

        /* code specific for each django app */
        switch (this.env.app) {
            case 'accounts': {
                break;
            }

            case 'dashboard': {
                break;
            }
        }
    };

    /* lock all controls on a form */
    this.lock_form = function (form, lock) {
        if (!form || !form.elements) return ;
        var n,
        len,
        elm;
        if (lock) this.disabled_form_elements = [
        ];
        for (n = 0, len = form.elements.length; n < len; n++) {
            elm = form.elements[n];
            if (elm.type == 'hidden') continue;
            if (lock && elm.disabled) this.disabled_form_elements.push(elm);
             else if (lock || $.inArray(elm, this.disabled_form_elements) < 0) elm.disabled = lock
        }
    };
}