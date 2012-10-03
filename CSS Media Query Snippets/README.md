Sublime Text CSS Media Query Snippets
===========================

A collection of media query snippets for common use cases.  Included snippets:

* Desktop/Laptop
* Ipad (general)
* Ipad Landscape
* Ipad Portrait
* Smartphone (general)
* Iphone 4 (retina)
* Smartphone Portrait
* Smartphone Landscape

The `trigger` for each snippet is in the format `media query XXX` where **XXX** is the name of each snippet. So you could type e.g. "med" then ctrl+space to trigger the snippets and select the one you want, or keep typing e.g. _por_ and the portrait snippets will pop up.

They look like this:
```
    /* iPads (portrait) ----------- */
    @media only screen
    and (min-device-width : 768px) 
    and (max-device-width : 1024px) 
    and (orientation : portrait) {
        ${1:/* Styles */}
    }
```

where the ${1} makes the cursor immediately jump to that spot so you can begin editing your styles.

Feedback welcome, this is my first (teeny tiny) sublime package but it may be useful for someone else.