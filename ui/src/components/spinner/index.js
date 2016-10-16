import 'font-awesome/css/font-awesome.css'

export default {
  name: 'Spinner',
  template: '<i v-show="spinning" class="fa fa-spinner fa-spin"></i>',
  props: ['spinning'],
}
