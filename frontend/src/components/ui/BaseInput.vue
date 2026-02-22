<template>
  <div>
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <div class="relative">
      <div v-if="$slots.prefix" class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400">
        <slot name="prefix" />
      </div>
      <input
        :id="inputId"
        ref="input"
        v-bind="$attrs"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="[
          'w-full rounded-xl border text-sm transition-all duration-200 focus:outline-none focus:ring-2',
          error
            ? 'border-red-300 focus:border-red-500 focus:ring-red-200'
            : 'border-gray-200 focus:border-primary-500 focus:ring-primary-100',
          disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white hover:border-gray-300',
          $slots.prefix ? 'pl-10' : 'pl-4',
          $slots.suffix ? 'pr-10' : 'pr-4',
          sizeClasses,
        ]"
        @input="onInput($event)"
      />
      <div v-if="$slots.suffix" class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
        <slot name="suffix" />
      </div>
    </div>
    <p v-if="error" class="mt-1 text-xs text-red-500">{{ error }}</p>
    <p v-else-if="hint" class="mt-1 text-xs text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed, ref, useId } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  modelModifiers: { type: Object, default: () => ({}) },
  label: { type: String, default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  error: { type: String, default: '' },
  hint: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  required: { type: Boolean, default: false },
  size: { type: String, default: 'md' },
})

const emit = defineEmits(['update:modelValue'])

function onInput(event) {
  let value = event.target.value
  if (props.type === 'number' || props.modelModifiers?.number) {
    const parsed = parseFloat(value)
    value = isNaN(parsed) ? value : parsed
  }
  emit('update:modelValue', value)
}

const input = ref(null)
const inputId = useId()

const sizeClasses = computed(() => {
  const map = {
    sm: 'py-1.5',
    md: 'py-2.5',
    lg: 'py-3',
  }
  return map[props.size] || map.md
})

defineExpose({ focus: () => input.value?.focus() })
</script>
