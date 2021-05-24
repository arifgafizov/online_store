var app = new Vue({
    el: '#appProduct',
    data: {
      products: [],
      product: '',
      product_detail: [],
      isActive: false,
      isAuth: false
    },
    methods: {
      onProduct: function (product_id){
        this.isActive = true
        axios.get('/api/v1/products/' + product_id).then(response => {
            console.log(response)
//          добавление в product_detail детализации товара полученного из response data
            this.product_detail = response.data
            console.log(this.product_detail)
          })
      },
      addToCart: function (product_id) {
//          сохранение в переменной токена авторизации полученного из localStorage
            const token = localStorage.getItem('AUTH_TOKEN')
//          отправка пост запроса с данными username и password из формы
          axios.post('/api/v1/cart-products/', {
                'product': product_id
            },
                {
                    headers: {
                        Authorization: "Token " + token
                    },
                }
            ).then((response) => {

            console.log(response)

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
          this.isAuth = true
          this.checkAuthLoading = false
       }).catch((err) => {
          if (err.response?.status === 401) {
          } else {
        }
      })
     },

    mounted() {
          axios.get('/api/v1/products/', {
            }).then(response => {
            console.log(response)
//          добавление в products списка товаров полученного из response data results
            this.products = response.data.results
            console.log(this.products)
          })
     }
})