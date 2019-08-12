<template>
    <div class="container chat">
        <nav class="navbar navbar-light bg-primary">
            <h2 class="text-light text-center">Chatapp</h2>
            <h5 class="text-light text-center"></h5>
        </nav>
        
        <div class="card set">
            <div class="card-body">
                <p class="text-light nomessages" v-if="messages.length == 0">
                    [No messages yet!]
                </p>
                <div class="messages" v-chat-scroll="{always: false, smooth: true, scrollonremoved: true}">
                    <div v-for="message in messages" :key="message.id">
                        <div class="row">
                            <div class="col-1">
                            <img src="../assets/chat-bubble.png" alt="avatar" v-if="message.name == 'bot'">
                            <img src="../assets/user.png" alt="avatar" v-else>
                            </div>
                            <div class="col-10">
                                <div class="border border-primary rounded-bottom bg-light">
                                    <span class="text-info">{{ message.name }} </span>
                                    <pre >{{message.message}}</pre>
                                    <span class="text-secondary time">{{message.timestamp}}</span>
                                </div>    
                            </div>
                        </div> 
                    </div>  
                </div>
            </div>
            
        </div>
        <div class="card-action">
            <CreateMessage :name="name"/>
        </div>
    </div>
</template>

<script>
import CreateMessage from '@/components/CreateMessage';
import fb from '@/firebase/init';
import moment from 'moment';

export default {
    name: 'Chat',
    props: ['name'],
    components: {
        CreateMessage
    },
    data() {
        return {
            messages: [],
            message:[]
        }
    },
    created() {
        let ref = fb.collection('messages').orderBy('timestamp');

        ref.onSnapshot(snapshot => {
            snapshot.docChanges().forEach(change => {
                if (change.type = 'added') {
                    let doc = change.doc;
                    this.messages.push({
                        id: doc.id,
                        name: doc.data().name,
                        message: doc.data().message,
                        timestamp: moment(doc.data().timestamp).format('LTS')
                    });
                }
            });
        });
        console.log(ref);
        
    },
    mounted() {
        console.log('App mounted!');
        if (localStorage.getItem('message')) this.message = JSON.parse(localStorage.getItem('message'));
    },
    watch: {
        messages: {
            handler() {
                console.log('message changed!');
                localStorage.setItem('message', JSON.stringify(this.messages));
            },
            deep: true,
        },
    },
}
</script>

<style>
img{
    width: 50px;
    height: 50px;
}
.chat h2{
    font-size: 2.6em;
    margin-bottom: 0px;
}
pre {
    overflow-x: auto;
    white-space: pre-wrap;
    white-space: -moz-pre-wrap !important;
    white-space: -pre-wrap;
    white-space: -o-pre-wrap;
    word-wrap: break-word;
    background: #fff;
    margin: 10px;
}
.chat h5{
    margin-top: 0px;
    margin-bottom: 40px;
}

.chat span{
    font-size: 1.2em;
}

.chat .time{
    display: block;
    font-size: 0.7em;
}

.messages{
    max-height: 450px;
    overflow: auto;
    overflow-x: hidden;
}
.row{
    margin-bottom: 10px;
}
.set{
    width: 100%;
    height: 500px;
    background-image: url(../assets/img.jpg);
    background-repeat: no-repeat;
    background-size: 100% 100%;
    border: 1px solid red;
}
</style>
