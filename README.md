# synoptico

[![Coverage Status](https://coveralls.io/repos/eldarion/timemap/badge.png?branch=master)](https://coveralls.io/r/eldarion/timemap?branch=master)
[![Build Status](https://magnum.travis-ci.com/eldarion/timemap.svg?token=VQrzBbxW2oucsNHSsdwY&branch=master)](https://magnum.travis-ci.com/eldarion/timemap)

The basic idea is that we collect a bunch of mappings between when an event occurs in the book and when in occurs in the films and then come up with cool ways of visualizing it.

So at the core is an event like "Bilbo finds the ring" which then gets mapped to some offset into the book and some offset into the films.

The initial crowdsourced gathering of data involves creating and verifying those events and mappings.

## Offsets into the Book

The challenge here is handling different editions. Interestingly, if we have mappings of events to different editions we end up with mappings between editions, not just between book and film. So it might be worth treating each edition as a different timeline an event can be mapped to. For a given edition we could map to page number, but do chapters also play a role here? Do we go any more fine-grained than page number?

## Offsets into the Films

I think this is fairly easy. We can treat theatrical and extended editions of films separately but in all cases it's basically film number + time offset into film.

## Event Scope

We should encourage "events" to be as punctiliar as possible. If a event spanning multiple pages is to be captured, best to either break it down or treat the "start" and "end" as separate events. The relationship *between* events could be worked on later. I think it's initially outside of the scope.

## Verification / Review

I think there are a number of different things that could be wrong with a mapping: the timeline reference could just be wrong, the event could have typos or be nonsense or bad English, there could be duplicates.

We could potentially punt on duplication issues. At one level it doesn't really matter if there is a "Bilbo finds the ring" AND a "Baggins finds the One Ring" as long as the mappings to book and film are correct. We *could* add handling of duplicates but I think that's a stretch goal (I've always liked the way the 43things, etc sites handled this if we do decide to do it). We still need to handle flagging errors.

Perhaps for things like typos, we just treat it as an error with a new submission but it would be nice to credit the original submitter too.

## Data Model

I'm thinking we have a Timeline, Event and a TimelineMapping model, plus models for review / flagging.

A Timeline is either a film or book with a mediatype and edition details plus creation metadata.

The Event just as a description plus creation metadata.

TimelineMapping has an FK to an event, an FK to Timeline and some machine-readable offset (page number / timecode) relevant to the mediatype of the Timeline plus creation metadata.

We then have the review flagging models. Might be worth a call to discuss those.
