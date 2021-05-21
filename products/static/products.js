var app = new Vue({
    el: '#appProduct',
    data: {
      products: [],
      product_detail: [],
      isActive: false
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
      }
    },
     mounted() {
          axios.get('/api/v1/products/').then(response => {
            console.log(response)
//          добавление в products списка товаров полученного из response data results
            this.products = response.data.results
            console.log(this.products)
          })
     }
})