-- À exécuter dans Supabase (SQL Editor) si le journal reste vide alors que
-- codes-acces.html est bien configuré : les INSERT navigateur étaient souvent
-- refusés par une politique trop restrictive selon le rôle effectif.

DROP POLICY IF EXISTS "Allow anon insert guide access log" ON public.guide_access_attempts;
DROP POLICY IF EXISTS "Allow insert guide access log" ON public.guide_access_attempts;

-- Politique sans cible de rôle explicite : s’applique aux rôles clients PostgREST
CREATE POLICY "Allow insert guide access log"
ON public.guide_access_attempts
FOR INSERT
WITH CHECK (true);

GRANT INSERT ON public.guide_access_attempts TO anon;
GRANT INSERT ON public.guide_access_attempts TO authenticated;
GRANT USAGE ON SCHEMA public TO anon;
GRANT USAGE ON SCHEMA public TO authenticated;
