import { defineCollection, z } from 'astro:content';

const policiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    id: z.string(),
    title: z.string(),
    type: z.string(),
    summary: z.string().optional(),
    hazard_type: z.array(z.string()).optional(),
    level_of_government_applicability: z.array(z.string()).optional(),
    implementation_horizon: z.string().optional(),
    fiscal_profile: z.object({
      cost_range: z.string(),
      cost_type: z.string()
    }).optional(),
    language: z.string().default('en')
  })
});

export const collections = {
  'policies': policiesCollection,
};
