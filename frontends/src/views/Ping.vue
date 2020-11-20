<template>
  <div class="container">
    <buttion type="button" class="btn btn-primary">{{ msg }}</buttion>
  </div>
</template>

<script>
import Axios from 'axios'


export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage(){
      const path = 'http://localhost:5000/ping';
      Axios.get(path)
          .then((res) => {
            this.msg = res.data;
          })
          .catch((error) =>{
            console.error(error);
          });
    },
  },
  created() {
    this.getMessage();
  }
};
</script>