fuzzify
=======

rSync fuzzy file pool manager

rSync does a wonderful job of finding like files using it's `--fuzzy` flag in a transfeterred files directory but does not properly index and scour through the entire file set to find matching files.  The result of this not happening is when files move or are removed from a file set and replaced again rSync loses the ability to match up remote content and further save bandwidth.

fuzzify simply sets up a pool as a temporary directory where hard links of the file set are grouped into directories representing the file size (or optionally an sha256 sum of the contents) and named similarly to eachother so that rSync can easily find and match up files that have a high possibility of being the same throughout the entire file set.

Once fuzzify has been run both locally and remotely under the source and destination directory then rSync can be run again with the ``--hard-links`` flag on on the entire file set where the pool is processed first due to its alphanumerically tuned directory name of ``...fuzzify```.

With any luck, and in an office environment there will be plenty of opportunity, files that have moved will not be retransferred to the remote location.

The fuzzify prep time is a consideration of course if you are planning on backing up files.  It runs quickly, hopefully it runs fast enough to make the bandwidth savings worth it in your situation.

You can optionally have fuzzify run in dirty mode.  When files are removed from the file set they will persist in a way in the fuzzify pool where when they are restored to the file set there is a high likelyhood that rsync will find a match.  It is probably not desirable to keep the pool dirty for very long due to it retaining all files via hard link each time the pool is refreshed.

Example Session
---------------

On Local:

.. code::

  fuzzify --logging=debug /sourcedir/
  
On Remote:

.. code::

  fuzzify --logging=debug /destdir/

The rSync:

.. code::

  rsync -avPHS --human-readable --stats --fuzzy /sourcedir/...fuzzify /sourcedir/ remote:/destdir/ --delete --delete-after

Then just remove ...fuzzify in sourcedir and destdir as needed.
