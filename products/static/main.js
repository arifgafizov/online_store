var app = new Vue({
    el: '#app',
    data: {
      todos: [
        { text: 'Apple' },
        { text: 'Grape' },
        { text: 'Peach' }
      ],
      username: '',
      password: '',
      isAuthenticated: false
    },
    methods: {
        onSubmit: function (username, password) {
            axios.post('/api/v1/users/auth/login/', {
                'username': username,
                'password': password,
            }).then(function(response) {
                console.log(response)
            }).catch(function(error) {
                console.log(error)
                alert(error)
            })
        }
    },
    created() {
     axios.get('/api/v1/users/auth/current/')
       .then(({data}) => {
          console.debug(data)
          this.checkAuthLoading = false
       }).catch((err) => {
          if (err.response?.status === 404) {

            this.isAuthenticated = true


          } else {
        }
      })
     }
})