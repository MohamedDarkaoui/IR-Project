<template>
  <div class="app-container">
    <div class="controls">
        <div class="search-container">
                <button class="toggle" @click="showEmotions = !showEmotions">Emotions {{showEmotions ? '˄' : '˅'}}</button>
                <input class="qinput" v-on:keyup.enter="search" type="text" v-model="q"/>
                <button @click="search">Search</button>
        </div>
        <div class="slider-container" v-show="showEmotions">
                <div class="sliderwrap" v-for="(emotion, key) in emotions" :key="emotion">
                        <p>{{emotion['lte'].toFixed(2)}}</p>
                        <div class="slidbar"></div>
                        <p>{{emotion['gte'].toFixed(2)}}</p>
                        <h>{{key}}</h>
                </div>
        </div>

    </div>
    <div class="display">

        <div v-if="searchResult">
        <div class="image-grid">
          <div v-for="result in searchResult" :key="result.text">
            <div class="container">
              <img class="image" v-bind:title="result.text"  :src="result.links[0]"/>
              <div class="overlay">
                <div class="text">{{result.text}}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

    </div>

  </div>
</template>

<script>
import Rangebar from 'rangebar';
import axios from 'axios';
import distinctColors from 'distinct-colors';

export default {
  data() {
    
    return {
      emotions : {
          "admiration": {'gte': 0, 'lte': 1},
          "amusement": {'gte': 0, 'lte': 1},
          "anger": {'gte': 0, 'lte': 1},
          "annoyance": {'gte': 0, 'lte': 1},
          "approval": {'gte': 0, 'lte': 1},
          "caring": {'gte': 0, 'lte': 1},
          "confusion": {'gte': 0, 'lte': 1},
          "curiosity": {'gte': 0, 'lte': 1},
          "desire": {'gte': 0, 'lte': 1},
          "disappointment": {'gte': 0, 'lte': 1},
          "disapproval": {'gte': 0, 'lte': 1},
          "disgust": {'gte': 0, 'lte': 1},
          "embarrassment": {'gte': 0, 'lte': 1},
          "excitement": {'gte': 0, 'lte': 1},
          "fear": {'gte': 0, 'lte': 1},
          "gratitude": {'gte': 0, 'lte': 1},
          "grief": {'gte': 0, 'lte': 1},
          "joy": {'gte': 0, 'lte': 1},
          "love": {'gte': 0, 'lte': 1},
          "nervousness": {'gte': 0, 'lte': 1},
          "optimism": {'gte': 0, 'lte': 1},
          "pride": {'gte': 0, 'lte': 1},
          "realization": {'gte': 0, 'lte': 1},
          "relief": {'gte': 0, 'lte': 1},
          "remorse": {'gte': 0, 'lte': 1},
          "sadness": {'gte': 0, 'lte': 1},
          "surprise": {'gte': 0, 'lte': 1},
          "neutral": {'gte': 0, 'lte': 1}
      },
      q: '',
      searchResult: null,
      showEmotions: true
    }
    
  },
  computed: {
    currentValue: {
      get() {
        return this[this.emotion];
      },
      set(value) {
        this[this.emotion] = value;
      }
    }
  },

  methods: {
    search() {

      axios.get('/api/emotionsearch',{
        params:{
          query: this.q,
          emotions: JSON.stringify(this.emotions)
        }
      })
      .then(responce => {
        this.searchResult = responce.data
        for (let result in this.searchResult){
          this.searchResult[result]['links'] = this.searchResult[result]['links'].split(',')
          console.log(this.searchResult[result]['links'])
        }
      })
      .catch(error => {
        console.error(error)
      })
    }
  },
  mounted(){
    console.log('mounted');

    let that = this;

    let bars = document.getElementsByClassName("slidbar")

    let palette = distinctColors({count:bars.length, lightMin: 50});
    console.log(palette)
    for (let i=0; i<bars.length; i++){
        let col = palette[i]._rgb;
        let r = col[0];
        let g = col[1];
        let b = col[2];

        new Rangebar({
          target: bars[i],
          data: {
            style: {
              // defualts
              len: '8em',
              width: '7px',
              barBackgroundColor: '#222',
              buttonBackgroundColor: 'rgb('+r.toString()+','+g.toString()+','+b.toString()+')'
            },
            horizontal: false, // or false (vertical) (default: true)
            min: 0, // minimum value (defualt: 0)
            max: 100, // maximum value (default: 100)
            buttons: [
              // specify init position (required)
              0,
              100,
            ],
            onChange(values) {
              let max = 1-values[0] / 100;
              let min = 1-values[1] / 100;
              let keys = Object.keys(that.emotions);

              that.emotions[keys[i]]['gte'] = min;
              that.emotions[keys[i]]['lte'] = max;
            }
          }
        });
    }

  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  grid-gap: 2px;
}

.container {
  position: relative;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.image {
  display: block;
  width: 100%;
  height: auto;
  margin-left: auto;
  margin-right: auto;
}

.overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  width: 100%;
  opacity: 0;
  transition: .5s ease;
}

.container:hover .overlay {
  opacity: 1;
}

.text {
  color: white;
  font-size: 30px;
  position: absolute;
  top: 20%;
  left: 50%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  text-align: center;
  background-color: black;
}

.app-container{
  @apply
    flex
    flex-col
}
.controls{
  @apply flex flex-col flex-auto justify-center items-center mb-8
}

.slider-container{
  @apply flex flex-row justify-center flex-wrap mt-8
}
.sliderwrap{
  @apply basis-32 flex flex-col items-center
}
.sliderwrap > h {
  @apply font-bold
}

.qinput{
  @apply text-2xl w-96 h-16 px-4 rounded-lg border-2
}

.search-container > button{
  @apply rounded-xl p-4 bg-sky-600 text-white mx-4 text-xl
}

</style>
