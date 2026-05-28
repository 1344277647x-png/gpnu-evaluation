<template>
  <div class="star-rating" @mouseleave="hoverIdx = 0">
    <span
      v-for="i in 5"
      :key="i"
      class="star"
      :class="starClass(i)"
      @click="!readonly && $emit('update:modelValue', i)"
      @mouseenter="!readonly && (hoverIdx = i)"
    >&#9733;</span>
    <span v-if="showValue" class="star-value">{{ modelValue }} / 5</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: Number, default: 0 },
  showValue: { type: Boolean, default: false },
  readonly: { type: Boolean, default: false }
})
defineEmits(['update:modelValue'])

const hoverIdx = ref(0)

function starClass(i) {
  if (!props.readonly && hoverIdx.value) return i <= hoverIdx.value ? 'active' : ''
  return i <= props.modelValue ? 'active' : ''
}
</script>

<style scoped>
.star-rating {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}
.star {
  font-size: 24px;
  color: #d1d5db;
  cursor: pointer;
  transition: color 0.15s;
  user-select: none;
}
.star.active {
  color: #f59e0b;
}
.star-value {
  margin-left: 8px;
  font-size: 14px;
  color: #6b7280;
}
</style>
