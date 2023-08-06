(window.webpackJsonp=window.webpackJsonp||[]).push([[74],{166:function(module,__webpack_exports__,__webpack_require__){"use strict";var index_es=__webpack_require__(169);__webpack_require__.d(__webpack_exports__,"a",function(){return struct});const struct=Object(index_es.a)({types:{"entity-id":function(value){if("string"!==typeof value){return"entity id should be a string"}if(!value.includes(".")){return"entity id should be in the format 'domain.entity'"}return!0},icon:function(value){if("string"!==typeof value){return"icon should be a string"}if(!value.includes(":")){return"icon should be in the format 'mdi:icon'"}return!0}}})},171:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return configElementStyle});var lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(41);const configElementStyle=lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
  <style>
    paper-toggle-button {
      padding-top: 16px;
    }
    .side-by-side {
      display: flex;
    }
    .side-by-side > * {
      flex: 1;
      padding-right: 4px;
    }
  </style>
`},739:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"HuiMarkdownCardEditor",function(){return HuiMarkdownCardEditor});var lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(41),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(78),_polymer_paper_input_paper_textarea__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(183),_common_structs_struct__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(166),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(154),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(65),_config_elements_style__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(171);const cardConfigStruct=Object(_common_structs_struct__WEBPACK_IMPORTED_MODULE_3__.a)({type:"string",title:"string?",content:"string"});class HuiMarkdownCardEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_4__.a)(lit_element__WEBPACK_IMPORTED_MODULE_0__.a){setConfig(config){config=cardConfigStruct(config);this._config=config}static get properties(){return{hass:{},_config:{}}}get _title(){return this._config.title||""}get _content(){return this._config.content||""}render(){if(!this.hass){return lit_element__WEBPACK_IMPORTED_MODULE_0__.c``}return lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      ${_config_elements_style__WEBPACK_IMPORTED_MODULE_6__.a}
      <div class="card-config">
        <paper-input
          label="Title"
          .value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <paper-textarea
          label="Content"
          .value="${this._content}"
          .configValue="${"content"}"
          @value-changed="${this._valueChanged}"
          autocapitalize="none"
          autocomplete="off"
          spellcheck="false"
        ></paper-textarea>
      </div>
    `}_valueChanged(ev){if(!this._config||!this.hass){return}const target=ev.target;if(this[`_${target.configValue}`]===target.value){return}if(target.configValue){if(""===target.value){delete this._config[target.configValue]}else{this._config=Object.assign({},this._config,{[target.configValue]:target.value})}}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_5__.a)(this,"config-changed",{config:this._config})}}customElements.define("hui-markdown-card-editor",HuiMarkdownCardEditor)}}]);
//# sourceMappingURL=0488833a52ea0581394d.chunk.js.map