<template>
	<div class="msd-container" v-click-outside="closeDropdown">
	  	<div class="selectedOptionsBox" v-on:click="toggleDropdown">
	  		<span class="label">{{ label +':' }}</span>
	  		<span class="selectedOption" v-model="selectedOptionsText">{{ selectedOptionsText }}</span>
	  		<div v-bind:class="{upArrow: true, downArrow: dropdownOpen }"></div>
	  	</div>
	  	<div class="dropdown" v-show="dropdownOpen">
		  	<ul>
		  		<li class="allOption" v-on:click="clearSelected">{{ 'All ' + label }}<div class="checkmark" v-show="selected.length === 0">&#x1F5F8;</div>
			    <li class="listOption" v-for="option in options" v-on:click="toggleSelect(option)">{{ Array.isArray(options) ? option : option.name }}<div class="checkmark" v-show="selected.includes(option)">&#x1F5F8;</div></li>
			</ul>
		</div>
	</div>
</template>

<script>
  import ClickOutside from 'vue-click-outside'
  export default {
    name: 'multi-select-dropdown',
    directives: {
      ClickOutside
    },
    props: {
      options: {
        type: [Array, Object],
        required: true
      },
      label: {
      	type: String,
      	required: false
      }
    },
    data() {
      return {
      	selected: [],
      	dropdownOpen: false
      }
    },
    computed: {
    	selectedOptionsText () {
    		let text = ''
    		if (this.selected.length === 0 || this.selected.length === this.options.length) {
    			text = 'All ' + this.label
    		} else {
    			if (!Array.isArray(this.options)) {
    				for (let s of this.selected) {
    					text += s.name + ', '
    				}
    				text = text.substring(0, text.length-2)
    			}
    			else {
    				text = this.selected.join(',')
    			}
    		}
    		return text
    	}
    },
    methods: {
    	toggleDropdown () {
    		this.dropdownOpen = !this.dropdownOpen
    	},
    	closeDropdown () {
    		this.dropdownOpen = false
    	},
    	toggleSelect (option) {
    		if (!this.selected.includes(option)) {
    			this.selected.push(option)
    			if (this.selected.length === this.options.length || this.selected.length === Object.keys(this.options).length) {
    				this.clearSelected()
    			}
    		} else {
    			let index = this.selected.indexOf(option)
    			this.selected.splice(index,1)
    		}
    	},
    	clearSelected () {
    		this.selected = []
    	}
    }
  }
</script>

<style scoped>
	.msd-container {
		position: relative;
		display: inline-block;
		vertical-align: middle;
		font-size: .9em
	}
	.selectedOptionsBox {
		background-color: #19181A;
		display: inline-block;
		padding-top: .5em;
		padding-bottom: .5em;
		width: 100%;
	}
	.upArrow {
		width: 0;
		border: 5px solid;
		border-color: transparent;
		border-top-color: white;
		position: absolute;
		right: 10px;
		top: 1em;
	}
	.downArrow {
		border-top-color: transparent;
		border-bottom-color: white;
		top: .5em;
	}
	.dropdown {
		background-color: #19181A;
	}
 	ul {
 		width: 100%;
		list-style: none;
		position: absolute;
		z-index: 999;
		display: flex;
		flex-direction: column;
		vertical-align: middle;
		padding-left: 0;
		margin: 0;
		background-color: inherit;
	}
	ul > li {
		display: block;
		padding: .5em;
	}
	.listOption {
		display: block;
		padding: .5em;
	}
	ul > li:hover {
		background-color: rgba(50, 48, 52, 1);
	}
	.label {
		padding: .5em;
	}
	.checkmark {
		display: inline-block;
		position: absolute;
		right: 10px;
	}
</style>
