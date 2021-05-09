var app = new Vue({
    el: '#app',
    data: {
      todos: [
        { text: 'Apple' },
        { text: 'Grape' },
        { text: 'Peach' }
      ]
    },
    created() {
     axios.get('/usersdata/user-data/')
      .then(({data}) => {
        console.debug(data)
        this.checkAuthLoading = false
      }).catch((err) => {
        if (err.response?.status === 401) {

      } else {
      }
    })
    }
})