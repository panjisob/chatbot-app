<template>
    <div class="panel-footer bg-dark pos">
        <form @submit.prevent="createMessage">
            <div class="input-group mb-3">    
                <input id="btn-input" type="text" class="form-control chat_input" placeholder="Write your message here..." v-model="newMessage" aria-label="Recipient's username" aria-describedby="basic-addon2"/>
                <div class="input-group-append">
                <button class="btn btn-primary btn-sm" type="submit" id="btn-chat"><i class="fa fa-send fa-1x" aria-hidden="true"></i></button>
                </div>
            </div>
        </form>
    </div>
</template>

<style>
.pos{
    padding: 10px;
}
form{
    margin-top: 10px;
}
</style>


<script>
import fb from '@/firebase/init';
import axios from 'axios';

export default {
    name: 'CreateMessage',
    props: ['name'],
    data() {
        return {
            message: [],
            newMessage: null,
            errorText: null,
            res: []
        };
        messages = [] 
    },
    methods: {
        createMessage () {
            var cuy = this;
            if (this.newMessage) {
                // cuy.message.push({pesan: this.newMessage, name: this.name, timestamp: Date.now() });
                const path = 'http://localhost:9001/chat';
                const chat = {
                    me: this.newMessage
                };
                fb.collection('messages').add({
                    message: this.newMessage,
                    name: this.name,
                    timestamp: Date.now()
                }).catch(err => {
                    console.log(err);
                });
                this.newMessage = null;
                this.errorText = null;

                axios.post(path, chat)
                    .then((res) => {
                    this.res = res;
                    console.log(res.data.text);
                    
                    fb.collection('messages').add({
                        message: res.data.text,
                        name: "bot",
                        timestamp: Date.now()
                    }).catch(err => {
                        console.log(err);
                    });
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.error(error);
                });
            } else {
                this.errorText = "A message must be entered first!";
            }
        }
    },
    // mounted() {
    //     console.log('App mounted!');
    //     if (localStorage.getItem('message')) this.message = JSON.parse(localStorage.getItem('messege'));
    // },
    // watch: {
    //     message: {
    //     handler() {
    //         console.log('message changed!');
    //         localStorage.setItem('message', JSON.stringify(this.message));
    //     },
    //     deep: true,
    //     },
    // }    
}
</script>

