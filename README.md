# whiteboard

Requirements: You are supposed to design your own protocols for a real-time interactive
whiteboard app. For evaluation, you need to implement a prototype of the whiteboard app using the
protocols, and test its performance.

The whiteboard application is supposed to
- allow any user to create a new session and invite others to join the session. The user who has
created the session would serve as the host and can accept or decline the requests for joining
the session. The session would end when the host leaves or ends the session.
- allow for freehand drawing and support the Erase and Undo functions.
- allow multiple users (more than 2 users) to draw on the same board at the same time.
- provide a consistent (shared) view for all the users in the same session.
- allow users to add, edit, or remove sticky notes.
- allow users to upload images and to comment on the images. Comments can be texts
attached to the images, or drawing on the images.
- allow users to save the whiteboard as a JPEG or PNG file before ending the session

The protocols are expected to be light-weight and secured. 
