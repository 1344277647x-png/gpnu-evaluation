<template>
  <div class="login-illust">
    <svg viewBox="0 0 300 240" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="lgSky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#ecfdf5"/>
          <stop offset="100%" stop-color="#d1fae5"/>
        </linearGradient>
      </defs>
      <rect width="300" height="240" fill="url(#lgSky)" rx="16"/>

      <!-- desk -->
      <rect x="80" y="145" width="140" height="10" rx="3" fill="#d4a373"/>
      <rect x="85" y="155" width="8" height="40" rx="2" fill="#c08a5e"/>
      <rect x="207" y="155" width="8" height="40" rx="2" fill="#c08a5e"/>

      <!-- laptop -->
      <rect x="105" y="115" width="90" height="6" rx="2" fill="#374151"/>
      <rect x="100" y="120" width="100" height="28" rx="3" fill="#4b5563"/>
      <rect x="106" y="126" width="88" height="16" rx="1" fill="#10b981"/>
      <!-- screen content -->
      <rect x="118" y="130" width="60" height="3" rx="1" fill="#fff" opacity="0.7"/>
      <rect x="118" y="135" width="45" height="2" rx="1" fill="#fff" opacity="0.4"/>
      <circle cx="195" cy="133" r="5" fill="#fff" opacity="0.3"/>

      <!-- student -->
      <circle cx="150" cy="95" r="14" fill="#fbbf24"/>
      <ellipse cx="150" cy="97" rx="14" ry="4" fill="#f59e0b" opacity="0.3"/>
      <path d="M130 108 Q150 95 170 108" fill="#fbbf24"/>
      <!-- eyes -->
      <circle cx="144" cy="93" r="2" fill="#1f2937"/>
      <circle cx="156" cy="93" r="2" fill="#1f2937"/>
      <!-- smile -->
      <path d="M145 99 Q150 103 155 99" fill="none" stroke="#1f2937" stroke-width="1.2" stroke-linecap="round"/>

      <!-- arms -->
      <line x1="125" y1="115" x2="115" y2="125" stroke="#fbbf24" stroke-width="4" stroke-linecap="round"/>
      <line x1="175" y1="115" x2="185" y2="125" stroke="#fbbf24" stroke-width="4" stroke-linecap="round"/>

      <!-- stars -->
      <g fill="#f59e0b" opacity="0.7">
        <text x="60" y="55" font-size="16">★</text>
        <text x="225" y="60" font-size="13">★</text>
        <text x="40" y="100" font-size="11">★</text>
      </g>

      <!-- plant -->
      <rect x="245" y="130" width="20" height="25" rx="3" fill="#d4a373"/>
      <circle cx="255" cy="120" r="10" fill="#10b981"/>
      <circle cx="248" cy="115" r="7" fill="#34d399"/>
      <circle cx="262" cy="117" r="6" fill="#059669"/>

      <!-- coffee cup -->
      <rect x="218" y="138" width="14" height="12" rx="2" fill="#fff"/>
      <path d="M232 140 Q236 144 232 148" fill="none" stroke="#fff" stroke-width="2"/>
      <ellipse cx="225" cy="138" rx="6" ry="2" fill="#6b7280"/>
    </svg>
  </div>
</template>

<style scoped>
.login-illust { width: 100%; max-width: 300px; margin: 0 auto; }
.login-illust svg { width: 100%; height: auto; display: block; }
</style>
