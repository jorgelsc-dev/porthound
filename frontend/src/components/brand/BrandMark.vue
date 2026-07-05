<template>
  <div
    class="brand-mark"
    :class="{
      'brand-mark--animated': animated,
      'brand-mark--framed': framed,
      'brand-mark--glow': glow,
    }"
    :style="sizeStyle"
  >
    <svg
      class="brand-mark__svg"
      viewBox="0 0 512 512"
      xmlns="http://www.w3.org/2000/svg"
      :role="decorative ? undefined : 'img'"
      :aria-label="decorative ? undefined : label"
      :aria-hidden="decorative ? 'true' : undefined"
    >
      <defs>
        <linearGradient
          :id="gradientId"
          gradientUnits="userSpaceOnUse"
          x1="72"
          y1="64"
          x2="438"
          y2="462"
        >
          <stop offset="0%" stop-color="#0fe8ff" />
          <stop offset="34%" stop-color="#20c9ff" />
          <stop offset="69%" stop-color="#4b8fff" />
          <stop offset="100%" stop-color="#8e63ff" />
          <animateTransform
            v-if="animated"
            attributeName="gradientTransform"
            type="translate"
            values="-72 0;72 0;-72 0"
            dur="4.6s"
            repeatCount="indefinite"
          />
        </linearGradient>
        <filter
          :id="glowId"
          x="-30%"
          y="-30%"
          width="160%"
          height="160%"
        >
          <feGaussianBlur stdDeviation="8" result="blur" />
          <feColorMatrix
            in="blur"
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.45 0"
          />
        </filter>
      </defs>

      <g v-if="glow" opacity="0.42" :filter="`url(#${glowId})`">
        <path :d="OUTLINE_PATH" :fill="`url(#${gradientId})`" fill-rule="evenodd" />
        <path :d="EYE_RING_PATH" :fill="`url(#${gradientId})`" fill-rule="evenodd" />
        <path :d="EYE_DOT_PATH" :fill="`url(#${gradientId})`" />
      </g>

      <g>
        <path :d="OUTLINE_PATH" :fill="`url(#${gradientId})`" fill-rule="evenodd" />
        <path :d="EYE_RING_PATH" :fill="`url(#${gradientId})`" fill-rule="evenodd" />
        <path :d="EYE_DOT_PATH" :fill="`url(#${gradientId})`" />
      </g>
    </svg>
  </div>
</template>

<script>
const OUTLINE_PATH = "M 215.0,45.5 L 225.0,48.5 L 235.5,64.0 L 243.5,99.0 L 246.5,125.0 L 250.0,129.5 L 275.5,88.0 L 286.5,73.0 L 297.0,62.5 L 302.0,59.5 L 309.0,58.5 L 318.5,65.0 L 324.5,80.0 L 325.5,99.0 L 321.5,137.0 L 312.5,173.0 L 330.0,185.5 L 339.5,196.0 L 346.5,210.0 L 348.5,224.0 L 352.0,227.5 L 421.0,270.5 L 428.5,278.0 L 432.5,287.0 L 432.5,295.0 L 428.5,307.0 L 413.5,331.0 L 397.0,347.5 L 380.0,356.5 L 369.0,358.5 L 352.0,357.5 L 287.0,341.5 L 283.0,341.5 L 279.5,345.0 L 279.5,354.0 L 284.5,375.0 L 303.5,430.0 L 304.5,447.0 L 297.0,458.5 L 287.0,464.5 L 276.0,467.5 L 263.0,468.5 L 242.0,465.5 L 224.0,459.5 L 205.0,450.5 L 103.0,387.5 L 91.0,379.5 L 82.5,369.0 L 82.5,361.0 L 85.5,349.0 L 116.5,239.0 L 132.5,207.0 L 148.5,188.0 L 148.5,157.0 L 152.5,139.0 L 159.5,119.0 L 172.5,92.0 L 189.5,66.0 L 204.0,50.5 Z M 215.0,63.5 L 207.5,70.0 L 192.5,91.0 L 173.5,131.0 L 166.5,160.0 L 166.5,196.0 L 161.0,199.5 L 148.5,213.0 L 134.5,239.0 L 113.5,309.0 L 99.5,360.0 L 99.5,365.0 L 190.0,422.5 L 225.0,441.5 L 251.0,450.5 L 274.0,451.5 L 284.0,448.5 L 287.5,445.0 L 288.5,441.0 L 283.5,420.0 L 268.5,378.0 L 264.5,362.0 L 263.5,348.0 L 258.0,343.5 L 238.0,335.5 L 232.0,331.5 L 224.5,322.0 L 229.0,320.5 L 263.0,330.5 L 268.0,330.5 L 277.0,326.5 L 290.0,325.5 L 316.0,330.5 L 353.0,340.5 L 374.0,340.5 L 391.0,331.5 L 405.5,316.0 L 413.5,302.0 L 414.5,289.0 L 408.0,281.5 L 339.0,237.5 L 332.5,230.0 L 332.5,217.0 L 328.5,207.0 L 315.0,192.5 L 293.0,180.5 L 264.0,172.5 L 238.0,168.5 L 232.5,164.0 L 231.5,133.0 L 227.5,102.0 L 221.5,76.0 Z M 305.0,77.5 L 294.5,89.0 L 262.5,140.0 L 255.5,153.0 L 259.0,156.5 L 296.0,165.5 L 298.5,163.0 L 303.5,145.0 L 308.5,109.0 L 308.5,84.0 Z";
const EYE_RING_PATH = "M 188.0,210.5 L 201.0,212.5 L 211.0,217.5 L 222.5,230.0 L 228.5,247.0 L 226.5,263.0 L 218.5,277.0 L 207.0,286.5 L 190.0,291.5 L 181.0,290.5 L 166.0,283.5 L 156.5,273.0 L 152.5,265.0 L 149.5,252.0 L 152.5,236.0 L 159.5,225.0 L 169.0,216.5 Z M 183.0,230.5 L 179.0,232.5 L 170.5,243.0 L 170.5,259.0 L 174.5,266.0 L 180.0,270.5 L 193.0,272.5 L 201.0,268.5 L 205.5,264.0 L 208.5,256.0 L 208.5,246.0 L 205.5,239.0 L 199.0,232.5 L 195.0,230.5 Z";
const EYE_DOT_PATH = "M 283.0,211.5 L 291.0,212.5 L 299.0,216.5 L 304.5,222.0 L 308.5,231.0 L 305.5,244.0 L 301.0,249.5 L 295.0,252.5 L 282.0,251.5 L 277.0,248.5 L 266.5,236.0 L 265.5,229.0 L 267.5,222.0 L 275.0,214.5 Z";
let brandMarkSequence = 0;

export default {
  name: "BrandMark",
  props: {
    size: {
      type: [Number, String],
      default: 56,
    },
    animated: {
      type: Boolean,
      default: false,
    },
    framed: {
      type: Boolean,
      default: false,
    },
    glow: {
      type: Boolean,
      default: true,
    },
    label: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      OUTLINE_PATH,
      EYE_RING_PATH,
      EYE_DOT_PATH,
      instanceId: ++brandMarkSequence,
    };
  },
  computed: {
    baseId() {
      return `brand-${this.instanceId}`;
    },
    decorative() {
      return !String(this.label || "").trim();
    },
    gradientId() {
      return `${this.baseId}-gradient`;
    },
    glowId() {
      return `${this.baseId}-glow`;
    },
    sizeStyle() {
      const value = typeof this.size === "number" ? `${this.size}px` : String(this.size || "56px");
      return { "--brand-mark-size": value };
    },
  },
};
</script>

<style scoped>
.brand-mark {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--brand-mark-size, 56px);
  height: var(--brand-mark-size, 56px);
  flex: 0 0 auto;
}

.brand-mark__svg {
  display: block;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.brand-mark--glow::after {
  content: "";
  position: absolute;
  inset: 8%;
  border-radius: 999px;
  background: radial-gradient(
    circle,
    rgba(var(--brand-cyan-rgb), 0.18),
    rgba(var(--brand-violet-rgb), 0) 70%
  );
  filter: blur(16px);
  z-index: -1;
}

.brand-mark--animated::after {
  animation: brand-mark-halo 2.4s ease-in-out infinite;
}

.brand-mark--framed {
  padding: 10px;
  border-radius: 18px;
  border: 1px solid rgba(var(--brand-sky-rgb), 0.18);
  background:
    radial-gradient(circle at 22% 18%, rgba(var(--brand-cyan-rgb), 0.16), transparent 44%),
    radial-gradient(circle at 82% 84%, rgba(var(--brand-violet-rgb), 0.18), transparent 46%),
    linear-gradient(145deg, rgba(10, 17, 28, 0.94), rgba(8, 13, 22, 0.84));
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.03),
    0 14px 28px rgba(2, 7, 13, 0.22);
}

@keyframes brand-mark-halo {
  0%,
  100% {
    transform: scale(0.92);
    opacity: 0.42;
  }
  50% {
    transform: scale(1.06);
    opacity: 0.84;
  }
}
</style>
