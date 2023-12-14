import { authentication, createDirectus, readItem, readItems, rest } from '@directus/sdk';

async function setupDirectus(url: string, email: string, password: string) {
  const directus = createDirectus(url).with(authentication()).with(rest());
  await directus.login(email, password);
  return { directus, readItem, readItems };
}

export default defineNuxtPlugin(async () => {
  const config = useRuntimeConfig();
  const { directus, readItem, readItems } = await setupDirectus(
    config.public.API_URL,
    config.public.API_EMAIL,
    config.public.API_PASSWD,
  );
  return {
    provide: { directus, readItem, readItems },
  };
});
