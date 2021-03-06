(function($) {
    $.fn.eventSelector = function(options) {
        var settings = $.extend({}, options);
        return this.each(function() {
            var $form = $(this);
            var $hidden = $("input[name=event_pk]", $form);
            var $typeahead = $("input[name=event_description]", $form);
            var cached_streams = null;
            var selected = null;
            $typeahead.typeahead(
                {
                    hint: false,
                    highlight: true
                },
                {
                    source: function(q, cb) {
                        var findMatches = function(events) {
                            // @@@ Implement fuzzy or ngram matching
                            var matches = [];
                            $.each(events, function(i, event) {
                                if ($.trim(event.description).toLowerCase().indexOf($.trim(q).toLowerCase()) > -1) {
                                    matches.push(event);
                                }
                            });
                            if (matches.length === 0) matches.push({description: q, pk: "[new]"});
                            cb(matches);
                        };
                        if (cached_streams === null) {
                            $.get($typeahead.data("ac-url"), function(data) {
                                cached_streams = data;
                                findMatches(cached_streams);
                            });
                        } else {
                            findMatches(cached_streams);
                        }
                    },
                    templates: {
                        suggestion: function(obj) {
                            if (obj.pk == "[new]") {
                                return "<div class='result'><span class=\"unbold\"><i class=\"fa fa-plus\"></i> Create new event:</span> <strong>" + obj.description + "</strong></div>";
                            }
                            mappings = "";
                            $.each(obj.mappings, function(i, mapping) {
                                mappings += "<div class='mapping'><span class='offset'>" + mapping.offset + "</span> &mdash; <span class='timeline'>" + mapping.timeline + "</span></div>";
                            });
                            return "<div class='result'><div class='event'>" + obj.description + "</div><div class='mappings'>" + mappings + "</div></div>";
                        }
                    }
                }
            )
            .on("typeahead:selected", function(e, datum, ds) {
                $hidden.val(datum.pk);
                $typeahead.val(datum.description);
                selected = datum.description;
                $(this).data("prev-value", $(this).val());
            })
            .on("propertychange keyup input paste", function(e) {
                if ($(this).data("prev-value") != $(this).val()) {
                    $hidden.val("");
                    $(this).data("prev-value", $(this).val());
                }
            })
            .on("blur", function (e) {
                $(this).val(selected);  // HACK: typeahead clears the input on blur for some reason
            });
        });
    };
})(jQuery);
