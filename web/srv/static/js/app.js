new Vue({
    el: '#app',

    data: {
        ws: null, // Our websocket
        newMsg: '', // Holds new messages to be sent to the server
        messages: [] // A running list of chat messages displayed on the screen
    },

    created: function() {
        var self = this;
        this.ws = new WebSocket('ws://' + window.location.host + '/ws');
        this.ws.addEventListener('message', function(e) {
            var data = JSON.parse(e.data);
            if(data.messages){
              self.messages = self.messages.concat(data.messages);
            }
            // self.chatContent += '<div class="chip">'
            //         + '<img src="' + self.gravatarURL(msg.email) + '">' // Avatar
            //         + msg.username
            //     + '</div>'
            //     + emojione.toImage(msg.message) + '<br/>'; // Parse emojis
            //
            // var element = document.getElementById('chat-messages');
            // element.scrollTop = element.scrollHeight; // Auto scroll to the bottom
        });
    },

    methods: {
        send: function () {
            if (this.newMsg !== '') {
              var msg = {
                email: this.email,
                username: this.username,
                message: $('<p>').html(this.newMsg).text() // Strip out html
              };
              this.ws.send(JSON.stringify(msg));
              this.newMsg = ''; // Reset newMsg
            }
        },

        join: function () {
          console.log("entered join")
          // this is where you'll put your lds details
            // if (!this.email) {
            //     Materialize.toast('You must enter an email', 2000);
            //     return
            // }
            // if (!this.username) {
            //     Materialize.toast('You must choose a username', 2000);
            //     return
            // }
            // this.email = $('<p>').html(this.email).text();
            // this.username = $('<p>').html(this.username).text();
            // this.joined = true;
        }
    }
});
