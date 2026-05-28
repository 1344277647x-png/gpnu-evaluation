<template>
  <div ref="chartRef" :style="{ width: '100%', height: height + 'px' }"></div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  ratings: { type: Object, default: () => ({ teaching: 0, content: 0, exam: 0, fairness: 0 }) },
  height: { type: Number, default: 320 }
})

const chartRef = ref(null)
let chartInstance = null

function initChart() {
  if (!chartRef.value) return
  if (chartInstance) chartInstance.dispose()

  chartInstance = echarts.init(chartRef.value)
  const r = props.ratings
  const hasData = r.teaching > 0 || r.content > 0 || r.exam > 0 || r.fairness > 0

  chartInstance.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, data: ['Score'] },
    radar: {
      center: ['50%', '48%'],
      radius: '65%',
      indicator: [
        { name: 'Teaching', max: 5 },
        { name: 'Content', max: 5 },
        { name: 'Exam', max: 5 },
        { name: 'Fairness', max: 5 }
      ]
    },
    series: [{
      type: 'radar',
      data: [{
        value: hasData ? [r.teaching, r.content, r.exam, r.fairness] : [0, 0, 0, 0],
        name: 'Score',
        areaStyle: { color: 'rgba(16, 185, 129, 0.15)' },
        lineStyle: { color: '#10b981', width: 2 },
        itemStyle: { color: '#059669' }
      }]
    }]
  })

  window.addEventListener('resize', () => chartInstance?.resize())
}

onMounted(() => nextTick(initChart))
watch(() => props.ratings, () => nextTick(initChart), { deep: true })
</script>
