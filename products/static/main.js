var app = new Vue({
    el: '#app',
    data: {
      todos: [
        { text: 'Foo' },
        { text: 'Bar' }
      ],
      username: '',
      password: '',
      isAuthenticated: true
    },
    methods: {
        onSubmit: function () {
//          отправка пост запроса с данными username и password из формы
            axios.post('/api/v1/users/auth/login/', {
                'username': this.username,
                'password': this.password,
            }).then((response) => {
                console.log(response)
//              сохранение в переменной токена авторизации полученного из response data
                const token = response.data.token
//              добавление токена авторизации в localStorage с ключом AUTH_TOKEN
                localStorage.setItem('AUTH_TOKEN', token)
                this.isAuthenticated = true
            }).catch(function(error) {
                console.log(error)
                alert(error)
            })
        }
    },
    created() {
//    сохранение в переменной токена авторизации полученного из localStorage
     const token = localStorage.getItem('AUTH_TOKEN')
//     отправка гет запроса в заголовке которого токен авторизации
     axios.get('/api/v1/users/auth/current/', {
        headers: {
          Authorization: "Token " + token
          }
     })
       .then(({data}) => {
          console.debug(data)
          this.isAuthenticated = true
          this.checkAuthLoading = false
       }).catch((err) => {
          if (err.response?.status === 401) {

            this.isAuthenticated = false


          } else {
        }
      })
     }
})