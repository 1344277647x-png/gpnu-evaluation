<template>
  <div class="empty-state">
    <svg viewBox="0 0 200 140" xmlns="http://www.w3.org/2000/svg" class="empty-svg">
      <!-- clipboard -->
      <rect x="50" y="15" width="85" height="105" rx="6" fill="#d1fae5" stroke="#10b981" stroke-width="2"/>
      <rect x="75" y="5" width="35" height="14" rx="3" fill="#10b981"/>
      <!-- lines on clipboard -->
      <rect x="65" y="40" width="55" height="4" rx="2" fill="#a7f3d0"/>
      <rect x="65" y="52" width="45" height="4" rx="2" fill="#a7f3d0"/>
      <rect x="65" y="64" width="50" height="4" rx="2" fill="#a7f3d0"/>
      <rect x="65" y="76" width="35" height="4" rx="2" fill="#a7f3d0"/>
      <!-- star on clipboard -->
      <circle cx="120" cy="85" r="12" fill="#fef3c7"/>
      <text x="120" y="89" text-anchor="middle" font-size="14" fill="#f59e0b">★</text>

      <!-- small person looking at clipboard -->
      <circle cx="165" cy="60" r="9" fill="#6ee7b7"/>
      <path d="M152 72 Q165 62 178 72" fill="#6ee7b7"/>
      <circle cx="162" cy="58" r="1.5" fill="#047857"/>
      <circle cx="168" cy="58" r="1.5" fill="#047857"/>
    </svg>
    <p class="empty-text"><slot>暂无内容</slot></p>
  </div>
</template>

<style scoped>
.empty-state { text-align: center; padding: 24px 0; }
.empty-svg { width: 160px; height: auto; display: block; margin: 0 auto 12px; }
.empty-text { font-size: 14px; color: #9ca3af; }
</style>
