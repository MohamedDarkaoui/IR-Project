<template>
  <div class="app-container">
    <v-card elevation="2" class="controls">
        <div class="search-container">
                <span>K</span>
                <input class="K-select" type="number" v-model="K"/>
                <v-btn
                  class="mx-2"
                  fab
                  dark
                  small
                  large
                  @click="showEmotions = !showEmotions"
                  color="indigo"
                >
                  <v-icon dark>
                    mdi-emoticon
                  </v-icon>
                </v-btn>
                <input class="qinput" v-on:keyup.enter="search" type="text" v-model="q"/>
                <v-btn
                  class="mx-2"
                  fab
                  dark
                  small
                  large
                  @click="search"
                  color="purple"
                >
                  <v-icon dark>
                    mdi-magnify
                  </v-icon>
                </v-btn>
        </div>

        <div class="slider-container" v-show="showEmotions">
                <div class="sliderwrap" v-for="(emotion, key) in emotions" :key="emotion">
                        <p>{{emotion['lte'].toFixed(2)}}</p>
                        <div class="slidbar"></div>
                        <p>{{emotion['gte'].toFixed(2)}}</p>
                        <h class="cursor-pointer">{{key}}</h>
                </div>
        </div>
    </v-card>
    <div class="display">
        <div class="image-mason" v-if="searchResult">
<!--        <div class="image-grid">-->
<!--          <div v-for="result in searchResult" :key="result.text">-->
<!--            <div class="container">-->
<!--              <img class="image" v-bind:title="result.text"  :src="result.links[0]"/>-->
<!--              <div class="overlay">-->
<!--                <div class="text">{{result.text}}</div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->


              <v-img v-for="result in searchResult" :key="result.text" class="ai-img" :src="result.links[0]" @click="dialog = true;image=result;">
              </v-img>


         <v-dialog
            v-model="dialog"
            content-class="elevation-0"
            scrollable
          >
                 <v-card v-if="image !== null" dark>
                    <div class="image-content">
                      <div class="image-sidebar">
                        <v-textarea
                          outlined
                          label="Prompt"
                          :value="image.text"
                          readonly
                          no-resize
                          rows="10"
                        ></v-textarea>
                        <v-textarea
                          outlined
                          label="Emotions"
                          :value="ems"
                          readonly
                          no-resize
                          rows="15"
                        ></v-textarea>
                      </div>
                      <div class="image-carousel">
                                <v-carousel height="auto" style="width:auto">
                                  <v-carousel-item v-for="(link, i) in image.links" :key="i">
                                    <div class="flex flex-row justify-center w-full">
                                      <img class="big-image" :src="link"/>
                                    </div>

                                  </v-carousel-item>
                              </v-carousel>
                      </div>
                    </div>
                    <v-divider></v-divider>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="primary"
                        text
                        @click="dialog = false"
                      >
                        Close
                      </v-btn>
                    </v-card-actions>
                </v-card>
          </v-dialog>




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
      showEmotions: true,
      dialog: false,
      image: null,
      ems: "",
      K:50,
      selected_em: "",
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
   watch: {
    // whenever question changes, this function will run
    image(n, old) {
      if (n !== null) {
        this.ems = ""
        for (const [key, value] of Object.entries(this.emotions)) {
          let name = key.toString()
          name = name.padEnd(30, ' ')
          this.ems += name + " : " + this.image[key] +"\n";
        }

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
    setTimeout(()=>{
      this.showEmotions = false;
    }, 40)

  }

}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.app-container{
  @apply
    flex
    flex-col
    h-screen
}
.controls{
  background: rgb(53,60,77);
  background: radial-gradient(circle, rgba(76,86,110,1) 0%, rgba(53,60,77,1) 0%);
  border-color: rgba(53,60,77,1) !important;
  @apply flex flex-col flex-initial justify-center items-center py-4
}

.slider-container{
  @apply flex flex-row justify-center flex-wrap mt-8 text-white
}
.sliderwrap{
  @apply basis-32 flex flex-col items-center
}
.sliderwrap > h {
  @apply font-bold
}

.qinput{
  border-color: rgba(76,86,110,1) !important;
  @apply text-2xl w-96 h-16 px-4 rounded-lg border-2 border-solid text-white
}
.K-select{
  border-color: rgba(76,86,110,1) !important;
  @apply text-2xl w-24 px-4 rounded-lg border-2 border-solid text-white mr-4 ml-2
}
.search-container{
  @apply flex flex-row justify-center items-center text-white text-2xl
}
.display{
  @apply flex-auto overflow-y-auto
}
.image-mason{
  @apply columns-7 gap-x-2 px-2 pt-2
}
.ai-img{
  @apply mb-2 aspect-auto w-full rounded-md cursor-pointer hover:rounded-3xl hover:scale-105
}
.image-content{
  @apply flex flex-row px-8 pt-4
}
.image-sidebar{
  @apply basis-1/4 flex flex-col items-stretch
}
.image-carousel{
  @apply flex-auto flex flex-row justify-center
}
.big-image{
  @apply w-auto h-[80vh]
}
</style>
