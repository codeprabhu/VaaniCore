#include "mfcc.h"
#include <math.h>
#include <stddef.h>

#define N 512
#define MEL_BANDS 40
#define OUT 10
#define PI 3.14159265358979323846f
#define EPS 1.0e-8f

static float hz_to_mel(float hz) { return 2595.0f * log10f(1.0f + hz / 700.0f); }
static float mel_to_hz(float mel) { return 700.0f * (powf(10.0f, mel / 2595.0f) - 1.0f); }

void vaanicore_mfcc_frame(const float *samples, size_t count, float out[OUT]) {
  float hp[N], emphasized[N], power[N / 2 + 1], logmel[MEL_BANDS];
  float previous = 0.0f, hp_previous = 0.0f;
  for (size_t n = 0; n < N; ++n) {
    float sample = n < count ? samples[n] : 0.0f;
    hp[n] = sample - previous + 0.995f * hp_previous;
    previous = sample; hp_previous = hp[n];
  }
  emphasized[0] = hp[0];
  for (size_t n = 1; n < N; ++n) emphasized[n] = hp[n] - 0.97f * hp[n - 1];
  for (size_t k = 0; k <= N / 2; ++k) {
    float real = 0.0f, imag = 0.0f;
    for (size_t n = 0; n < N; ++n) {
      float value = emphasized[n] * (0.5f - 0.5f * cosf(2.0f * PI * (float)n / (float)(N - 1)));
      float angle = 2.0f * PI * (float)k * (float)n / (float)N;
      real += value * cosf(angle); imag -= value * sinf(angle);
    }
    power[k] = real * real + imag * imag;
  }
  float low_mel = hz_to_mel(20.0f), high_mel = hz_to_mel(4000.0f);
  for (size_t m = 0; m < MEL_BANDS; ++m) {
    float left_hz = mel_to_hz(low_mel + (high_mel - low_mel) * (float)m / (MEL_BANDS + 1));
    float center_hz = mel_to_hz(low_mel + (high_mel - low_mel) * (float)(m + 1) / (MEL_BANDS + 1));
    float right_hz = mel_to_hz(low_mel + (high_mel - low_mel) * (float)(m + 2) / (MEL_BANDS + 1));
    int left = (int)floorf((N + 1) * left_hz / 16000.0f);
    int center = (int)floorf((N + 1) * center_hz / 16000.0f);
    int right = (int)floorf((N + 1) * right_hz / 16000.0f);
    if (center <= left) center = left + 1;
    if (right <= center) right = center + 1;
    float energy = 0.0f;
    for (int k = left; k < center && k <= N / 2; ++k) if (k >= 0) energy += power[k] * (float)(k - left) / (float)(center - left);
    for (int k = center; k < right && k <= N / 2; ++k) if (k >= 0) energy += power[k] * (float)(right - k) / (float)(right - center);
    logmel[m] = logf(energy + EPS);
  }
  for (size_t k = 0; k < OUT; ++k) {
    out[k] = 0.0f;
    for (size_t m = 0; m < MEL_BANDS; ++m) out[k] += logmel[m] * cosf(PI * (float)k * (2.0f * (float)m + 1.0f) / (2.0f * MEL_BANDS));
  }
}
