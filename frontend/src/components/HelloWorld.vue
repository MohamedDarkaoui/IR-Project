<template>
  <div>
    <div v-for="emotion in emotions" :key="emotion">
      <div class="app">
        <div id="slider-container">
          <label>{{Object.keys(emotion)[0]}}</label>
          <input type="range" min="0" max="1" step="0.01" v-model="emotion.value" class="slider">
          <div>{{emotion.value}}</div>
        </div>
      </div>
    </div>
    <input type="text" v-model="q"/>
    <button @click="search">Search</button>
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
</template>

<script>
import axios from 'axios'
export default {
  data() {
    
    return {
      emotions : [
        {admiration: 0},
        {amusement: 0},
        {anger: 0},
        {annoyance: 0},
        {approval: 0},
        {caring: 0},
        {confusion: 0},
        {curiosity: 0},
        {desire: 0},
        {disappointment: 0},
        {disapproval: 0},
        {disgust: 0},
        {embarrassment: 0},
        {excitement: 0},
        {fear: 0},
        {gratitude: 0},
        {grief: 0},
        {joy: 0},
        {love: 0},
        {nervousness: 0},
        {optimism: 0},
        {pride: 0},
        {realization: 0},
        {relief: 0},
        {remorse: 0},
        {sadness: 0},
        {surprise: 0},
        {neutral: 0},
    ],
      q: '',
      searchResult: null
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

      axios.get('http://localhost:5000/api/normalsearch',{
        params:{
          query: this.q
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

.app{
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
</style>
