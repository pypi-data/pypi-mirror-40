/*jslint browser: true, plusplus: true */
/*global jQuery, moment */

var EMSAIU = (function ($) {
    "use strict";

    var term_lookahead = 4;

    // prep for api post/put
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function search_in_progress(selector) {
        var tpl = Handlebars.compile($("#ajax-waiting").html());
        $(selector).html(tpl());
    }

    function course_search_in_progress() {
        $("form.course-search button").attr('disabled', 'disabled');
        search_in_progress(".course-search-result");
    }

    function course_search_complete() {
        $("form.course-search button").removeAttr('disabled');
    }

    function api_path(service, params) {
        var query;

        var url = window.emsaiu.app_url + 'api/v1/' + service;

        if (params) {
            query = [];
            $.each(params, function (k, v) {
                query.push(k + '=' + encodeURIComponent(v));
            });
            url += '?' + query.join('&');
        }

        return url;
    }

    function paint_course_schedule(term, courses) {
        var tpl = Handlebars.compile($('#course-search-result-template').html()),
            context = {
                term: term.term_id,
                term_name: term.term_name,
                term_start: term.first_day_quarter,
                term_end: term.last_final_exam_date,
                schedule: [],
                tsv_url: api_path('aiu/' + term.term_id + '.txt')
            };

        window.emsaiu.courses = {};

        $.each(courses, function () {

            var course_start_date = moment(this.StartDate),
                course_end_date = moment(this.EndDate),
                now = moment();

            window.emsaiu.courses[this.CourseTitle] = this;

            context.schedule.push(this);
        });

        $('.course-search-result').html(tpl(context));
        $('.course-search-result table').DataTable({
            buttons: [{
                extend: 'csvHtml5',
                extension: '.txt',
                fieldBoundary: '',
                fieldSeparator: '\t',
                filename: term.term_id,
                header: false,
                newline: '\r\n',
                text: 'Download TSV',
            }],
            ordering: false,
            paging: false,
            dom: "<'row'<'col-sm-12'tr>>",
        }).buttons().container().appendTo( '.result-header .batchswitch' );
    }

    function failure_modal(title, default_text, xhr) {
        var tpl = Handlebars.compile($('#ajax-fail-tmpl').html()),
            modal_container,
            failure_text = default_text,
            err;

        if (xhr.hasOwnProperty('responseText')) {
            try {
                err = JSON.parse(xhr.responseText);

                if (err.hasOwnProperty('error')) {
                    failure_text = err.error;
                }
            } catch (ignore) {
            }
        }

        $('body').append(tpl({
            failure_title: title,
            failure_message: failure_text,
            full_failure_message: xhr.responseText
        }));

        modal_container = $('#failure-modal');
        modal_container.modal();
        modal_container.on('hidden.bs.modal', function () {
            $(this).remove();
        });
    }

    function course_search_failure(xhr) {
        $(".course-search-result").empty();
        failure_modal('Course schedule could not be found',
                      'Make sure the search terms are correct, and try again.',
                      xhr);
    }

    function set_course_search_criteria(course) {
    }

    function find_course(term) {
        $.ajax({
            type: 'GET',
            url: api_path('aiu/' + term.term_id),
            beforeSend: course_search_in_progress,
            complete: course_search_complete
        })
            .fail(course_search_failure)
            .done(function (msg) {
                $.extend(term, msg.term);
                paint_course_schedule(term, msg.records);
                set_course_search_criteria();
                history.pushState({}, '', '?term=' + term.term_id);
            });
    }

    function do_course_search(ev) {
        var term = {
            term_id: $('select#qtr-select').val().trim().toLowerCase(),
            term_name: $('select#qtr-select option:selected').text(),
        };

        if (ev) {
            ev.preventDefault();
        }

        find_course(term);
    }

    function update_term_selector() {
        /*jshint validthis: true */
        $('#selected-quarter').html($("option:selected", this).text());
    }

    function init_term_selector() {
        var quarters = ['winter', 'spring', 'summer', 'autumn'],
            year,
            i,
            j,
            s,
            t,
            opt;

        if (!$("select#qtr-select").length) {
            return;
        }

        year = window.emsaiu.term.year;
        j = quarters.indexOf(window.emsaiu.term.quarter.toLowerCase());
        for (i = 0; i < term_lookahead; i += 1) {
            s = quarters[j];
            t = s[0].toUpperCase() + s.slice(1) + ' ' + year;

            opt = $('<option></option>')
                    .text(t)
                    .attr('value', year + '-' + s)
                    .attr('title', 'Select ' + t)
                    .prop("selected", (i === 0) ? true : false);

            $("select#qtr-select").append(opt);

            if (++j >= quarters.length) {
                j = 0;
                year++;
            }
        }
        $("select#qtr-select").change(update_term_selector);
    }

    function initialize() {
        $.ajaxSetup({
            crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", window.emsaiu.csrftoken);
                }
            }
        });

        $("form.course-search").submit(do_course_search);
        init_term_selector();
        Handlebars.registerPartial('reservation-list', $('#reservation-list-partial').html());
    }

    $(document).ready(initialize);

    //return {
    //    initialize: initialize
    //};
}(jQuery));
