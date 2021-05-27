var app = new Vue({
    el: '#app',
    data: {
      cart_products: [],
      orders: [],
      cart_total_price: '',
      username: '',
      password: '',
      isAuthenticated: true,
      isActive: false,
      isOrderActive: false,
      phone: '',
      address: '',
      deliveryAt: ''
    },
    methods: {
        onSubmit: function () {
//          отправка пост запроса с данными username и password из формы
            axios.post('/api/v1/users/auth/login/', {
                'username': this.username,
                'password': this.password,
            }).then ((response) => {
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
        },

      onDeleteCartProduct (product_id) {
//          сохранение в переменной токена авторизации полученного из localStorage
        const token = localStorage.getItem('AUTH_TOKEN')
//        проходимся по cart_products используя find с функцией сравнения полученного product_id с id товара в корзине
//        сохраняя найденный товар в переменной product
        const product = this.cart_products.find(function (product) {
            return product.id === product_id
        })
//        сохраняем в переменной productPosition id позиции в корзине
        const productPosition = product.positions.pop().id
//        отправляем delete запрос с id позиции в корзине
        axios.delete('/api/v1/cart-products/' + productPosition, {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {
                console.log(response)
            }).catch(function(error) {
                console.log(error)
            })
      },

      onStartMakeOrder: function (){
        this.isOrderActive = true
      },

      onMakeOrder: function () {
//          сохранение в переменной токена авторизации полученного из localStorage
            const token = localStorage.getItem('AUTH_TOKEN')
//          отправка пост запроса с данными username и password из формы
          axios.post('/api/v1/orders/', {
                'phone': this.phone,
                'address': this.address,
                'delivery_at': this.deliveryAt
            },
                {
                    headers: {
                        Authorization: "Token " + token
                    },
                }
            ).then((response) => {
            this.isOrderActive = false
            console.log(response)

          }).catch(function(error) {
                console.log(error)
                alert(error)
            })
      },

      payOrder: function (order_id)  {
        //  открытие ссылки с передачей order_id в url params
        location.replace('/payments/pay-forms/?order-id=' + order_id)
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
     },
     mounted() {

          //    сохранение в переменной токена авторизации полученного из localStorage
          const token = localStorage.getItem('AUTH_TOKEN')
          //     отправка гет запроса в заголовке которого токен авторизации
//          получение товаров в корзине
          axios.get('/api/v1/cart-products/', {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {

            console.log(response)
//          добавление в cart_products списка товаров корзины полученного из response data
            this.cart_products = response.data
            console.log(this.cart_products)
          }),

//          получение общей цены товаров в корзине
          axios.get('/api/v1/cart-products/cart-total-price/', {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {

            console.log(response)
//          добавление в cart_products списка товаров корзины полученного из response data
            this.cart_total_price = response.data
            console.log(this.cart_total_price)
          }),

//          получение заказа
          axios.get('/api/v1/orders/', {
                headers: {
                    Authorization: "Token " + token
                }
            }).then(response => {

            console.log(response)
//          добавление в orders списка товаров корзины полученного из response data
            this.orders = response.data
            console.log(this.orders)
          })
     }
})