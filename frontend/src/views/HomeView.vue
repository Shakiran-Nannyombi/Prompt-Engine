<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
    <div class="container-wide py-12">
      <!-- Header -->
      <div class="text-center mb-16 animate-fade-in">
        <h1 class="text-5xl font-bold text-neutral-900 mb-6">
          Welcome to <span class="text-primary-600">Prompt Engine</span>
        </h1>
        <p class="text-xl text-neutral-700 max-w-2xl mx-auto leading-relaxed">
          AI-powered prompt engineering coach that guides you through a structured framework to craft high-quality prompts with intelligent refinement
        </p>
      </div>

      <!-- Agent Cards -->
      <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto mb-12">
        <!-- Coaching Agent Card -->
        <div class="card-base card-elevated card-interactive p-8">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex-center mb-6">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-neutral-900 mb-4">Prompt Engineering Coach</h2>
          <p class="text-neutral-700 mb-6 leading-relaxed">
            Master the art of prompt engineering with guided assistance through a structured 4-step process: Task → Context → References → Final Prompt
          </p>
          <ul class="text-sm text-neutral-700 mb-8 space-y-2">
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Structured 4-step coaching process
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Progress tracking and guidance
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Automatic grammar correction
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Final prompt refinement
            </li>
          </ul>
          <RouterLink to="/coaching" class="btn-primary">
            Start Coaching
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </RouterLink>
        </div>

        <!-- Refiner Agent Card -->
        <div class="card-base card-elevated card-interactive p-8">
          <div class="w-16 h-16 bg-secondary-100 rounded-full flex-center mb-6">
            <svg class="w-8 h-8 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-neutral-900 mb-4">Prompt Refiner Agent</h2>
          <p class="text-neutral-700 mb-6 leading-relaxed">
            Advanced prompt refinement with intelligent categorization and framework selection. Perfect for enhancing existing prompts.
          </p>
          <ul class="text-sm text-neutral-700 mb-8 space-y-2">
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Intelligent prompt categorization
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              C.O.R.E, R.A.C.E, C.A.R frameworks
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Document Q&A with RAG
            </li>
            <li class="flex items-center">
              <svg class="w-4 h-4 text-success-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Analysis view with insights
            </li>
          </ul>
          <RouterLink to="/refiner" class="btn-secondary">
            Start Refining
            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </RouterLink>
        </div>
      </div>

      <!-- Features Section -->
      <div class="text-center">
        <h2 class="text-2xl font-bold text-neutral-900 mb-8">Why Choose Prompt Engine?</h2>
        <div class="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div class="text-center">
            <div class="w-12 h-12 bg-success-100 rounded-full flex-center mx-auto mb-4 text-xl">
              💡
            </div>
            <h3 class="text-lg font-semibold text-neutral-900 mb-2">AI-Powered Intelligence</h3>
            <p class="text-neutral-700">Advanced LLM guidance with automatic grammar correction and intelligent analysis</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-primary-100 rounded-full flex-center mx-auto mb-4 text-xl">
              📈
            </div>
            <h3 class="text-lg font-semibold text-neutral-900 mb-2">Structured Approach</h3>
            <p class="text-neutral-700">Proven frameworks and methodologies for consistent, high-quality results</p>
          </div>
          <div class="text-center">
            <div class="w-12 h-12 bg-secondary-100 rounded-full flex-center mx-auto mb-4 text-xl">
              ⚡
            </div>
            <h3 class="text-lg font-semibold text-neutral-900 mb-2">Flexible & Powerful</h3>
            <p class="text-neutral-700">From beginner coaching to advanced refinement with document analysis</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>