

## Easy fixes

* The bird Emoji isn't really appropriate for Canberra. A Macaw parrot is featured very prominently. Just get rid of it.
* A generic/blanket attribution is showing everywhere (`Data from [Wikimedia Commons](https://commons.wikimedia.org), [Atlas of Living Australia](https://www.ala.org.au), [Xeno-canto](https://xeno-canto.org)
`) I don't like that. Just get rid of it.
* On the Information page (after IDing) other photos of the bird are shown. Mouse-over gives feedback as though it is interactive but clicking does nothing. Clicking should link to the image's source page but in a new tab.
* Don't show  'your stats' box in the main menu.
* Add a link to an about page on the main menu
* Just create a simple placeholder page for the about page
* Don't show the progress summary on the statistics page.

## Significant changes

* The scoring mechanism is a bit silly. Weshould just track right/wrong
* We haven't sourced any photos from ALA yet some species have just a few photos. We should try again to source photos from ALA.
* The audio recording are not playing.
    * Try to debug without changing the interface
    * Otherwise, I think we'll need to host them ourselves.
* The game is too easy! I shouldn't be able to win advanced mode. There's two factors:
    * Mostly really good quality photos (Let's keep it that way for now)
    * If you know a tiny bit about birds you can pretty reliably use the process of elimination to work out the multiple choice questions. For beginner mode this is awesome! For the harder difficulties we'll need to fix it by filtering the possible answers such that the species chosen are ones that are similar to the correct answer. We should do this taxonomically:
        * Closely related birds are easy to confuse.For hard difficulty we should prefer multiple choice options from the same genus. Where there aren't enough possibilities in the genus we should fall back on the family. If there aren't enough options in the family fall back to a random selection. For intermediate difficulty, prefer multiple choice options from the same family as the correct answer but also include random choices if there are two few members of the same family. 
* We're getting slow load times on the wikimedia commons images. I notice that we are using very high-res versions of the images. Solutions:
    * Wikimedia let's you specify a smaller image size (for example: `https://upload.wikimedia.org/wikipedia/commons/e/e0/Yellow_Tailed_Black_Cockatoo_02.jpg` or `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Yellow_Tailed_Black_Cockatoo_02.jpg/960px-Yellow_Tailed_Black_Cockatoo_02.jpg` or `https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Yellow_Tailed_Black_Cockatoo_02.jpg/330px-Yellow_Tailed_Black_Cockatoo_02.jpg`)
    * As an easy fix we can just use these smaller images.
  
## Hard problems (that will require human labour)

* The name canberra bird game is a bit lame.
* We've got no design assets. the favicon is generic.
* Some of the photos are innappropriate for bird ID. There are photos of eggs and dead birds. We need to fix this before the first release. We need a method for the human developer to easily review the photos. Let's make a browser-based tool that loads a big grid of thumbnail images. The interface will allow me to select a bunch of images and then download a JSON that identifies which ones I picked.
* I need to review the links page and make sure it is relevant and factual.
* I need to write an about page so that people can contact me to complain.