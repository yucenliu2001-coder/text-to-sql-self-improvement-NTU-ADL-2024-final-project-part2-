import re
medical_records = {
'Acute COPD exacerbation / infection':"""
Sex: Male, Age: 68
- I have a history of chronic obstructive pulmonary disease (COPD).
- I am experiencing shortness of breath or difficulty breathing in a significant way.
- I have a persistent cough.
- I am coughing up mucus, and its color has changed to yellow-green.
- I feel more fatigued than usual.
- I am wheezing more than usual.
- I have swelling in my legs or ankles.
- I have noticed a wheezing sound when I exhale.
- I feel like I can't get enough air even while resting.
- On a scale of 0-10, my difficulty breathing is 7
- On a scale of 0-10, my cough intensity is 6
- My chest feels tight and painful during coughing.
- The color of my mucus is yellow.
- On a scale of 0-10, my chest pain during coughing is 5
- The affected regions are:
* chest
* throat

**Reasoning:**
- The patient has a known history of COPD, which increases the risk of exacerbations.
- He is experiencing increased shortness of breath and wheezing, indicating worsening airway obstruction.
- The change in mucus color to yellow-green suggests a bacterial infection.
- Chest tightness and pain during coughing are common in COPD exacerbations.
- These symptoms point toward an acute COPD exacerbation likely triggered by an infection.
""",
'Acute dystonic reactions':"""
Sex: Female, Age: 28
- I recently started a new medication (antipsychotics).
- I am experiencing sudden muscle spasms or stiffness.
- I have difficulty moving my neck.
- My eyes are stuck looking upward.
- My jaw is clenched and painful.
- I feel like my tongue is stiff or swollen.
- I am unable to speak clearly due to muscle stiffness.
- On a scale of 0-10, my muscle stiffness is 8
- On a scale of 0-10, my pain intensity is 6
- The affected regions are:
  * neck
  * jaw
  * tongue
  * eyes

**Reasoning:**
- The patient recently began taking antipsychotic medication, which is known to cause extrapyramidal side effects like dystonia.
- She exhibits muscle stiffness and spasms in the neck, jaw, tongue, and eyes—typical regions affected in acute dystonic reactions.
- Symptoms such as oculogyric crisis (eyes stuck upward) and jaw clenching are characteristic.
- Difficulty speaking due to muscle stiffness further supports this diagnosis.
- The temporal association between medication initiation and symptom onset indicates a drug-induced dystonia.

""",
'Acute laryngitis':"""
Sex: Female, Age: 32
- I have been speaking a lot or shouting recently.
- I have a sore throat.
- My voice is hoarse or lost completely.
- I am coughing frequently.
- I have a fever.
- My throat feels dry and irritated.
- Swallowing is painful.
- On a scale of 0-10, my throat pain is 6
- On a scale of 0-10, my cough intensity is 5
- The color of my phlegm is clear.
- The affected regions are:
  * throat
  * vocal cords

**Reasoning:**
- Overuse of voice through speaking or shouting has strained the vocal cords.
- Hoarseness or loss of voice is a primary symptom of laryngitis.
- Sore throat, dryness, and painful swallowing indicate inflammation of the larynx.
- The presence of cough and fever suggests an acute infectious process.
- These findings are consistent with acute laryngitis, likely due to vocal strain and possible viral infection.

""",
'Acute otitis media':"""
Sex: Male, Age: 6
- I have been crying and pulling at my ear.
- I have ear pain.
- I have a fever.
- My hearing seems muffled.
- My ear feels full or blocked.
- I have ear discharge.
- I feel dizzy.
- On a scale of 0-10, my ear pain is 7
- On a scale of 0-10, my dizziness is 4
- The affected regions are:
  * ear (right)
  * ear canal

**Reasoning:**
- The patient is a child presenting with ear pain and pulling at the ear, common signs of ear discomfort in children.
- Fever and ear discharge suggest an infectious etiology.
- Muffled hearing and a feeling of fullness indicate fluid accumulation in the middle ear.
- Dizziness may result from inner ear involvement.
- These symptoms are characteristic of acute otitis media.

""",
'Acute pulmonary edema':"""
Sex: Male, Age: 65
- I have a history of heart failure.
- I am experiencing severe shortness of breath.
- I have noticed swelling in my legs and ankles.
- I am coughing up pink, frothy sputum.
- I feel dizzy and lightheaded.
- I am sweating excessively.
- My heart feels like it's racing.
- On a scale of 0-10, my difficulty breathing is 9
- On a scale of 0-10, my chest tightness is 8
- The color of my sputum is pink.
- The affected regions are:
  * chest
  * lungs
  * legs

**Reasoning:**
- The patient's history of heart failure predisposes him to fluid overload.
- Severe shortness of breath and pink, frothy sputum are hallmark signs of pulmonary edema.
- Peripheral edema (swelling in legs and ankles) indicates systemic fluid accumulation.
- Tachycardia and excessive sweating are responses to hypoxia and stress.
- These findings suggest acute pulmonary edema likely due to decompensated heart failure.

""",
'Acute rhinosinusitis':"""
Sex: Female, Age: 40
- I have facial pain, especially around my cheeks.
- My nose is congested.
- I have thick nasal discharge.
- I have a headache.
- I feel pressure around my eyes.
- I have a low-grade fever.
- On a scale of 0-10, my facial pain is 5
- On a scale of 0-10, my nasal congestion is 6
- The color of my nasal discharge is yellow-green.
- The affected regions are:
  * face
  * nasal passages
  * sinuses

**Reasoning:**
- Facial pain and pressure around the cheeks and eyes indicate sinus involvement.
- Nasal congestion with thick yellow-green discharge suggests bacterial infection of the sinuses.
- Headache and low-grade fever support the presence of an infection.
- The duration and acute onset point toward acute rhinosinusitis.
- These symptoms collectively align with acute rhinosinusitis.

""",
'Allergic sinusitis':"""
Sex: Female, Age: 25
- I have a known allergy to pollen or dust.
- I am sneezing frequently.
- My nose is runny and congested.
- My eyes are itchy and watery.
- I feel sinus pressure.
- My symptoms worsen when I'm outside.
- On a scale of 0-10, my nasal congestion is 6
- On a scale of 0-10, my sinus pressure is 5
- The affected regions are:
  * nose
  * sinuses
  * eyes

**Reasoning:**
- Known allergies to pollen or dust suggest an allergic etiology.
- Sneezing, runny nose, and itchy, watery eyes are classic allergic symptoms.
- Sinus pressure indicates inflammation of the sinus cavities.
- Symptoms worsening outdoors support exposure to environmental allergens.
- These findings are consistent with allergic sinusitis.

""",
'Anaphylaxis':"""
Sex: Male, Age: 35
- I have a known severe food allergy.
- I have been in contact with or ate something that I have an allergy to.
- I have experienced swelling in one or more areas of my body.
- I am experiencing shortness of breath or difficulty breathing in a significant way.
- I feel lightheaded and dizzy or I feel like I am about to faint.
- I lost consciousness.
- I have noticed a wheezing sound when I exhale.
- I have lesions, redness, or problems on my skin that I believe are related to the condition I am consulting for.
- I am more likely to develop common allergies than the general population.
- On a scale of 0-10, the pain intensity is 3
- On a scale of 0-10, the pain's location precision is 0
- On a scale of 0-10, the pace at which the pain appears is 10
- The color of the rash is red.
- On a scale of 0-10, the rash swelling is 8
- On a scale of 0-10, the pain intensity caused by the rash is 1
- The lesion (or lesions) are larger than 1cm.
- On a scale of 0-10, the severity of the rash itching is 7
- The pain is:
  * a stabbing sensation
- The pain locations are:
  * throat
  * chest
- The pain radiates to these locations:
  * jaw
  * shoulder(L)
- The affected regions are:
  * lips
  * eyelids
  * tongue
  * throat
  * neck
- The swelling locations are:
  * lips
  * eyelids
  * tongue
  * throat

**Reasoning:**
- Known severe food allergy with recent exposure indicates high risk for anaphylaxis.
- Swelling of lips, eyelids, tongue, and throat suggests angioedema.
- Significant difficulty breathing and wheezing point to airway compromise.
- Lightheadedness, dizziness, and loss of consciousness indicate hypotension.
- Skin manifestations like rash and itching are common in anaphylactic reactions.

""",
'Anemia':"""
Sex: Female, Age: 45
- I feel tired all the time.
- I feel dizzy when I stand up quickly.
- My skin looks pale.
- I get short of breath after mild activity.
- My heartbeat feels faster than usual.
- I feel weak and unable to lift heavy objects.
- On a scale of 0-10, my fatigue is 8
- On a scale of 0-10, my dizziness is 5
- The affected regions are:
  * whole body

**Reasoning:**
- Persistent fatigue and weakness suggest decreased oxygen delivery to tissues.
- Pallor is a common sign of anemia due to reduced hemoglobin.
- Dizziness upon standing indicates orthostatic hypotension from low blood volume or anemia.
- Tachycardia is a compensatory mechanism to maintain oxygenation.
- Shortness of breath after mild activity further supports anemia.

""",
'Atrial fibrillation':"""
Sex: Male, Age: 70
- I have a history of heart problems.
- My heart feels like it's fluttering or skipping beats.
- I feel tired and out of breath.
- I get dizzy when I stand up or move quickly.
- I have chest discomfort.
- I feel anxious and restless.
- On a scale of 0-10, my chest discomfort is 5
- On a scale of 0-10, my difficulty breathing is 7
- The affected regions are:
  * chest
  * heart

**Reasoning:**
- Palpitations described as fluttering suggest arrhythmia.
- History of heart problems increases the likelihood of atrial fibrillation.
- Fatigue and shortness of breath are symptoms of decreased cardiac efficiency.
- Dizziness upon movement indicates possible hypotension due to irregular heartbeat.
- These signs are consistent with atrial fibrillation.

""",
'Boerhaave':"""
Sex: Male, Age: 50
- I experienced severe vomiting or retching before this started.
- I have severe chest pain.
- I feel pain radiating to my back.
- I feel shortness of breath.
- My neck feels swollen or tender.
- I have noticed a crunching sound when pressing on my chest.
- On a scale of 0-10, my chest pain is 9
- On a scale of 0-10, my difficulty breathing is 7
- The affected regions are:
  * chest
  * neck
  * upper back

**Reasoning:**
- Severe vomiting followed by intense chest pain suggests possible esophageal rupture.
- Pain radiating to the back and neck swelling indicate mediastinal involvement.
- Subcutaneous emphysema (crunching sound on chest palpation) is a hallmark of Boerhaave syndrome.
- Shortness of breath may result from mediastinal air affecting lung expansion.
- These symptoms point toward spontaneous esophageal perforation (Boerhaave syndrome).

""",
'Bronchiectasis':"""
Sex: Female, Age: 55
- I have a persistent, productive cough.
- I am coughing up large amounts of yellow or green mucus.
- I feel short of breath when climbing stairs or walking.
- I get frequent chest infections.
- I sometimes cough up blood.
- My chest feels tight, and I hear wheezing when I breathe.
- On a scale of 0-10, my cough intensity is 8
- On a scale of 0-10, my chest tightness is 6
- The color of my mucus is green.
- The affected regions are:
  * chest
  * lungs

**Reasoning:**
- Chronic productive cough with large amounts of purulent sputum suggests bronchial damage.
- History of frequent chest infections indicates chronic respiratory condition.
- Hemoptysis (coughing up blood) is common in bronchiectasis due to damaged airway vessels.
- Wheezing and shortness of breath reflect airflow obstruction.
- These features are characteristic of bronchiectasis, involving permanent dilation of bronchi.

""",
'Bronchiolitis':"""
Sex: Male, Age: 1
- My breathing is noisy, and I wheeze a lot.
- I have a fever.
- I am coughing frequently.
- I am having difficulty feeding.
- My nostrils flare when I breathe.
- I seem tired and less active than usual.
- On a scale of 0-10, my breathing difficulty is 7
- On a scale of 0-10, my cough intensity is 5
- The affected regions are:
  * chest
  * nose

**Reasoning:**
- Infants presenting with wheezing and difficulty breathing are often experiencing bronchiolitis.
- Fever and cough suggest a viral infection, commonly RSV in this age group.
- Nasal flaring and feeding difficulties indicate increased respiratory effort.
- Fatigue and decreased activity are signs of systemic involvement.
- These symptoms are consistent with bronchiolitis affecting the small airways in infants.

""",
'Bronchitis':"""
Sex: Female, Age: 34
- I have been coughing for the last few days.
- My cough produces mucus.
- My chest feels sore and tight.
- I have a low-grade fever.
- I feel fatigued and short of breath.
- My throat feels dry and irritated.
- On a scale of 0-10, my cough intensity is 6
- On a scale of 0-10, my chest tightness is 5
- The color of my mucus is yellow.
- The affected regions are:
  * chest
  * throat

**Reasoning:**
- Acute onset of productive cough with yellow mucus suggests lower respiratory tract infection.
- Chest soreness from coughing indicates bronchial inflammation.
- Low-grade fever and fatigue support an infectious cause.
- Shortness of breath can occur due to airway inflammation.
- These symptoms align with acute bronchitis.

""",
'Bronchospasm / acute asthma exacerbation':"""
Sex: Male, Age: 25
- I have asthma and have had frequent flare-ups recently.
- I am wheezing when I breathe.
- I feel short of breath, even at rest.
- My chest feels tight and painful.
- I cough a lot, especially at night.
- I feel anxious because I can't catch my breath.
- On a scale of 0-10, my difficulty breathing is 8
- On a scale of 0-10, my chest tightness is 7
- The affected regions are:
  * chest
  * throat

**Reasoning:**
- Known asthma with recent frequent flare-ups indicates poorly controlled asthma.
- Wheezing and chest tightness are classic signs of bronchospasm.
- Nocturnal coughing is common in asthma exacerbations.
- Shortness of breath at rest signifies a severe episode.
- Symptoms are consistent with an acute asthma exacerbation involving bronchospasm.

""",
'Chagas':"""
Sex: Male, Age: 45
- I traveled to an area where Chagas disease is common.
- I have had a fever for several days.
- I feel tired and weak.
- My face is swollen, especially around the eye.
- I have mild chest pain and palpitations.
- My digestion seems slower than usual.
- On a scale of 0-10, my fatigue is 8
- On a scale of 0-10, my chest pain is 4
- The affected regions are:
  * chest
  * face
  * abdomen

**Reasoning:**
- The patient recently traveled to an endemic area for Chagas disease, increasing his risk of exposure.
- Swelling of the face, particularly around the eye (Romaña's sign), is characteristic of acute Chagas infection.
- Fever, fatigue, and weakness are common systemic symptoms during the acute phase.
- Mild chest pain and palpitations suggest early cardiac involvement, which is a known complication.
- Slowed digestion indicates possible gastrointestinal involvement due to parasitic effects on the enteric nervous system.
- These symptoms collectively point toward an acute Chagas disease diagnosis.

""",
'Chronic rhinosinusitis':"""
Sex: Female, Age: 42
- I have had nasal congestion and discharge for several weeks.
- My face feels full and heavy, especially around the cheeks.
- I have a headache that won't go away.
- My sense of smell is reduced.
- I feel tired and unwell.
- My throat feels irritated due to postnasal drip.
- On a scale of 0-10, my nasal congestion is 6
- On a scale of 0-10, my headache is 5
- The color of my nasal discharge is yellow.
- The affected regions are:
  * nasal passages
  * face
  * throat

**Reasoning:**
- Symptoms persisting for several weeks indicate a chronic condition.
- Facial fullness and persistent headache suggest ongoing sinus inflammation.
- Reduced sense of smell is common in chronic sinusitis.
- Postnasal drip causing throat irritation supports sinus involvement.
- Yellow nasal discharge indicates chronic inflammation or infection.

""",
'Cluster headache':"""
Sex: Male, Age: 38
- I have severe headaches on one side of my head.
- My eye waters and turns red during the headaches.
- My nose feels congested or runny during the headaches.
- The pain comes suddenly and is very intense.
- I feel restless and can't sit still during an attack.
- The headaches happen at the same time every day.
- On a scale of 0-10, my headache pain is 10
- On a scale of 0-10, my eye discomfort is 5
- The affected regions are:
  * head
  * eye (left)
  * nose

**Reasoning:**
- Unilateral severe headaches with autonomic symptoms (tearing, nasal congestion) suggest cluster headaches.
- Restlessness during attacks is typical for cluster headaches.
- The attacks occurring at the same time daily indicate a circadian pattern.
- Sudden onset and excruciating pain support this diagnosis.
- These features are characteristic of cluster headaches.

""",
'Croup':"""
Sex: Male, Age: 2
- I have a barking cough.
- I make a high-pitched noise when I breathe in (stridor).
- I have a fever.
- I am more tired than usual.
- My breathing seems faster and harder than normal.
- I am drooling more than usual.
- On a scale of 0-10, my breathing difficulty is 7
- On a scale of 0-10, my cough intensity is 6
- The affected regions are:
  * throat
  * chest

**Reasoning:**
- Barking cough and inspiratory stridor are classic signs of croup.
- Fever suggests an infectious etiology, often viral.
- Increased work of breathing and fatigue indicate respiratory distress.
- Drooling can occur due to difficulty swallowing.
- These symptoms are consistent with croup in a young child.

""",
'Ebola':"""
Sex: Male, Age: 29
- I recently traveled to an area with Ebola outbreaks.
- I have a high fever.
- I am vomiting and have diarrhea.
- I feel extremely weak and fatigued.
- I have noticed unusual bleeding from my gums or nose.
- My eyes look red.
- On a scale of 0-10, my fatigue is 9
- On a scale of 0-10, my fever discomfort is 8
- The affected regions are:
  * whole body
  * gums
  * eyes

**Reasoning:**
- Recent travel to an Ebola outbreak area significantly raises suspicion.
- High fever, vomiting, diarrhea, and severe fatigue are early symptoms of Ebola.
- Unusual bleeding indicates hemorrhagic manifestations of the disease.
- Conjunctival injection (red eyes) is a common sign.
- These findings are characteristic of Ebola virus infection.

""",
'Epiglottitis':"""
Sex: Male, Age: 7
- I have a severe sore throat.
- I have difficulty swallowing.
- I am drooling more than usual.
- I make a high-pitched noise when I breathe (stridor).
- I have a fever.
- I am experiencing significant difficulty breathing.
- On a scale of 0-10, my sore throat pain is 8
- On a scale of 0-10, my breathing difficulty is 9
- The affected regions are:
  * throat
  * neck

**Reasoning:**
- Severe sore throat with difficulty swallowing and drooling suggests inflammation of the epiglottis.
- Stridor and significant breathing difficulty indicate airway obstruction.
- High fever supports an acute infectious process.
- Age is within the common range for epiglottitis in children.
- These symptoms are indicative of epiglottitis, a medical emergency.

""",
'GERD':"""
Sex: Female, Age: 30
- I feel a burning sensation in my chest (heartburn).
- I often taste acid in my mouth.
- My symptoms worsen after eating or lying down.
- I have a chronic cough.
- My throat feels sore and irritated.
- I sometimes have difficulty swallowing.
- On a scale of 0-10, my heartburn intensity is 6
- On a scale of 0-10, my throat irritation is 4
- The affected regions are:
  * chest
  * throat
  * esophagus

**Reasoning:**
- Burning chest sensation and acid taste suggest acid reflux.
- Symptoms worsening after eating or lying down are typical for GERD.
- Chronic cough and sore throat indicate esophageal irritation from stomach acid.
- Difficulty swallowing can result from esophageal inflammation.
- These symptoms are consistent with gastroesophageal reflux disease (GERD).

""",
'Guillain-Barré syndrome':"""
Sex: Male, Age: 45
- I recently had a viral infection.
- I feel weakness starting in my legs.
- I have difficulty walking or climbing stairs.
- My arms feel weak as well.
- I feel tingling or pins-and-needles in my hands and feet.
- I sometimes have difficulty breathing.
- On a scale of 0-10, my weakness intensity is 7
- On a scale of 0-10, my tingling sensation is 5
- The affected regions are:
  * legs
  * arms
  * feet
  * hands

**Reasoning:**
- Recent viral infection is a common trigger for Guillain-Barré syndrome.
- Ascending muscle weakness starting from the legs is characteristic.
- Difficulty walking and climbing stairs indicate motor weakness.
- Tingling in extremities suggests peripheral nerve involvement.
- Breathing difficulties may occur if respiratory muscles are affected.

""",
'HIV (initial infection)':"""
Sex: Male, Age: 25
- I have a fever and feel very fatigued.
- I have a sore throat.
- I noticed a rash on my chest.
- My muscles and joints ache.
- My lymph nodes feel swollen.
- I have had night sweats recently.
- On a scale of 0-10, my fatigue is 8
- On a scale of 0-10, my sore throat pain is 5
- The affected regions are:
  * chest
  * lymph nodes
  * throat

**Reasoning:**
- Flu-like symptoms after potential exposure suggest acute HIV infection.
- Fever, fatigue, sore throat, and rash are common in seroconversion.
- Swollen lymph nodes indicate immune system activation.
- Night sweats are also associated with acute HIV infection.
- These symptoms align with the initial stage of HIV infection.

""",
'Influenza':"""
Sex: Female, Age: 29
- I have a fever and chills.
- I feel very tired and weak.
- My body aches, especially in my muscles.
- I have a cough and sore throat.
- My head feels heavy, and I have a headache.
- I feel nauseous and have little appetite.
- On a scale of 0-10, my fatigue is 8
- On a scale of 0-10, my headache is 6
- The affected regions are:
  * throat
  * chest
  * head

**Reasoning:**
- Sudden onset of fever, chills, and muscle aches are typical of influenza.
- Respiratory symptoms like cough and sore throat support a viral infection.
- Headache and severe fatigue further point toward influenza.
- Nausea and loss of appetite are common accompanying symptoms.
- These findings are consistent with the flu.

""",
'Inguinal hernia':"""
Sex: Male, Age: 60
- I have a bulge in my groin area.
- The bulge becomes more noticeable when I cough or lift something heavy.
- I feel pain in my groin.
- I feel heaviness in my lower abdomen.
- I sometimes feel nauseous.
- The bulge is tender when pressed.
- On a scale of 0-10, my groin pain is 6
- On a scale of 0-10, my discomfort is 5
- The affected regions are:
  * groin
  * lower abdomen

**Reasoning:**
- A groin bulge that worsens with coughing or lifting suggests an inguinal hernia.
- Pain and tenderness in the groin area support this.
- Heaviness in the lower abdomen is a common symptom.
- Nausea could indicate intermittent obstruction.
- These symptoms are characteristic of an inguinal hernia.

""",
'Laryngospasm':"""
Sex: Female, Age: 35
- I have a sensation of my throat closing suddenly.
- I feel like I can't catch my breath.
- I noticed a wheezing or high-pitched sound when I breathe.
- I feel anxious when this happens.
- My chest feels tight during these episodes.
- The episodes happen after eating or at night.
- On a scale of 0-10, my breathing difficulty is 8
- On a scale of 0-10, my chest tightness is 6
- The affected regions are:
  * throat
  * chest

**Reasoning:**
- Sudden throat closing sensation indicates possible laryngospasm.
- Wheezing and high-pitched sounds suggest upper airway obstruction.
- Anxiety and chest tightness are common during these episodes.
- Occurrence after eating or at night may indicate reflux triggering spasms.
- These findings are consistent with laryngospasm.

""",
'Localized edema':"""
Sex: Female, Age: 50
- I have swelling in my legs and ankles.
- The swelling worsens after standing for a long time.
- My skin feels tight and stretched in the swollen areas.
- The swollen area feels warm.
- I feel heaviness in my legs.
- I noticed a slight discoloration in the swollen area.
- On a scale of 0-10, my discomfort is 6
- On a scale of 0-10, my swelling severity is 7
- The affected regions are:
  * legs
  * ankles

**Reasoning:**
- Swelling in legs and ankles that worsens with standing suggests venous insufficiency.
- Tight, stretched skin and warmth indicate fluid accumulation.
- Heaviness and discoloration are common in localized edema.
- No systemic symptoms point toward a localized rather than generalized cause.
- These symptoms align with localized peripheral edema.

""",
'Myasthenia gravis':"""
Sex: Male, Age: 55
- I feel muscle weakness, especially in my arms and legs.
- My eyelids droop by the end of the day.
- I have difficulty swallowing food.
- I have trouble speaking clearly when I'm tired.
- My symptoms improve after rest.
- I sometimes feel short of breath.
- On a scale of 0-10, my muscle weakness is 7
- On a scale of 0-10, my difficulty swallowing is 5
- The affected regions are:
  * arms
  * legs
  * eyelids
  * throat

**Reasoning:**
- Muscle weakness that worsens with activity and improves with rest is characteristic of myasthenia gravis.
- Ptosis (drooping eyelids) by day's end suggests ocular involvement.
- Difficulty swallowing and speaking indicate bulbar muscle weakness.
- Shortness of breath may occur due to respiratory muscle involvement.
- These features are consistent with myasthenia gravis.

""",
'Myocarditis':"""
Sex: Male, Age: 40
- I feel chest pain that worsens when I lie down.
- I feel fatigued and short of breath.
- My heart feels like it's racing or skipping beats.
- I have a low-grade fever.
- My legs feel swollen.
- I sometimes feel lightheaded.
- On a scale of 0-10, my chest pain is 7
- On a scale of 0-10, my fatigue is 6
- The affected regions are:
  * chest
  * heart
  * legs

**Reasoning:**
- Chest pain worsening when lying down may indicate pericardial involvement.
- Arrhythmias (racing heart) suggest myocardial irritation.
- Fatigue, shortness of breath, and leg swelling indicate heart dysfunction.
- Low-grade fever points toward an inflammatory or infectious process.
- These symptoms are indicative of myocarditis.

""",
'PSVT':"""
Sex: Female, Age: 27
- I feel my heart racing suddenly without warning.
- I feel lightheaded and dizzy when it happens.
- I sometimes have chest discomfort.
- I feel short of breath during these episodes.
- I feel anxious and restless when my heart races.
- My symptoms stop abruptly after a few minutes.
- On a scale of 0-10, my chest discomfort is 4
- On a scale of 0-10, my dizziness is 6
- The affected regions are:
  * chest
  * heart

**Reasoning:**
- Sudden onset of rapid heart rate suggests paroxysmal supraventricular tachycardia (PSVT).
- Lightheadedness and dizziness occur due to decreased cardiac output during tachycardia.
- Shortness of breath and chest discomfort are common symptoms.
- Abrupt cessation of symptoms is typical for PSVT episodes.
- These findings are consistent with PSVT.

""",
'Pancreatic neoplasm':"""
Sex: Male, Age: 65
- I have persistent abdominal pain that radiates to my back.
- I have lost weight without trying.
- I feel nauseous and have little appetite.
- My skin and eyes look yellow (jaundice).
- I feel fatigued and weak.
- My stool appears pale and greasy.
- On a scale of 0-10, my abdominal pain is 7
- On a scale of 0-10, my fatigue is 6
- The affected regions are:
  * abdomen
  * back
  * skin

**Reasoning:**
- Persistent abdominal pain radiating to the back is common in pancreatic cancer.
- Unintentional weight loss and loss of appetite suggest malignancy.
- Jaundice indicates biliary obstruction, which can occur with pancreatic tumors.
- Pale, greasy stools point toward malabsorption due to pancreatic insufficiency.
- These symptoms are characteristic of a pancreatic neoplasm.

""",
'Panic attack':"""
Sex: Female, Age: 23
- I feel sudden fear or dread without a clear reason.
- My heart races, and I feel short of breath.
- I feel dizzy and lightheaded.
- My hands are trembling, and I am sweating profusely.
- I feel like I might faint or lose control.
- My chest feels tight, and I feel a choking sensation.
- On a scale of 0-10, my fear intensity is 9
- On a scale of 0-10, my chest tightness is 6
- The affected regions are:
  * chest
  * throat
  * hands

**Reasoning:**
- Sudden onset of intense fear and physical symptoms suggests a panic attack.
- Tachycardia, shortness of breath, and chest tightness are common physical manifestations.
- Trembling, sweating, and feelings of losing control further support this.
- No apparent trigger indicates it's psychological rather than physical.
- These symptoms are consistent with a panic attack.

""",
'Pericarditis':"""
Sex: Male, Age: 47
- I feel sharp chest pain that worsens when I lie down or take a deep breath.
- I feel short of breath.
- My heart feels like it is beating irregularly.
- I have mild fever and feel fatigued.
- The chest pain improves when I sit up or lean forward.
- On a scale of 0-10, my chest pain is 8
- On a scale of 0-10, my difficulty breathing is 6
- The affected regions are:
  * chest
  * heart

**Reasoning:**
- Chest pain worsening with lying down and improving when sitting up is classic for pericarditis.
- Pain exacerbated by deep breaths suggests involvement of the pericardial sac.
- Irregular heartbeat may result from pericardial inflammation affecting cardiac function.
- Mild fever and fatigue indicate an inflammatory process.
- These findings align with pericarditis.

""",
'Pneumonia':"""
Sex: Female, Age: 70
- I have a persistent cough that produces green mucus.
- I feel short of breath, even at rest.
- I have a fever and chills.
- My chest feels tight and painful when I breathe deeply or cough.
- I feel very fatigued and weak.
- I sometimes feel confused or disoriented.
- On a scale of 0-10, my cough intensity is 7
- On a scale of 0-10, my chest pain is 6
- The affected regions are:
  * chest
  * lungs

**Reasoning:**
- Productive cough with green mucus suggests a bacterial lung infection.
- Fever, chills, and chest pain are common in pneumonia.
- Shortness of breath at rest indicates significant lung involvement.
- Confusion in elderly patients can be a symptom of severe infection.
- These symptoms are consistent with pneumonia.

""",
'Possible NSTEMI / STEMI':"""
Sex: Male, Age: 58
- I feel severe chest pain that radiates to my left arm and jaw.
- I feel short of breath and sweaty.
- I feel nauseous and lightheaded.
- My chest pain feels like pressure or squeezing.
- The pain started suddenly and hasn’t improved with rest.
- On a scale of 0-10, my chest pain is 9
- On a scale of 0-10, my nausea is 5
- The affected regions are:
  * chest
  * left arm
  * jaw

**Reasoning:**
- Severe chest pain radiating to the left arm and jaw is classic for myocardial infarction.
- Pain described as pressure or squeezing supports cardiac origin.
- Lack of improvement with rest differentiates it from stable angina.
- Associated symptoms like sweating, nausea, and lightheadedness are common in heart attacks.
- These findings suggest a possible NSTEMI or STEMI.

""",
'Pulmonary embolism':"""
Sex: Female, Age: 45
- I feel sudden and severe shortness of breath.
- I feel sharp chest pain that worsens when I take a deep breath.
- I have a cough, and I noticed some blood in my mucus.
- My heart feels like it is racing.
- I feel lightheaded and close to fainting.
- I noticed swelling and redness in one of my legs.
- On a scale of 0-10, my difficulty breathing is 8
- On a scale of 0-10, my chest pain is 7
- The affected regions are:
  * chest
  * lungs
  * leg (left)

**Reasoning:**
- Sudden onset of severe shortness of breath and chest pain suggests an acute pulmonary issue.
- Chest pain worsening with deep breaths indicates pleuritic pain, common in pulmonary embolism.
- Hemoptysis (coughing up blood) is a classic symptom of pulmonary embolism.
- Tachycardia and lightheadedness are signs of hemodynamic compromise.
- Swelling and redness in the left leg suggest deep vein thrombosis as a source of the embolus.

""",
'Pulmonary neoplasm':"""
Sex: Male, Age: 64
- I have a chronic cough that sometimes produces blood.
- I feel chest pain that doesn’t go away.
- I have lost weight without trying.
- I feel fatigued and weak most of the time.
- I sometimes feel short of breath.
- I noticed my voice becoming hoarse.
- On a scale of 0-10, my cough intensity is 6
- On a scale of 0-10, my fatigue is 7
- The affected regions are:
  * chest
  * lungs

**Reasoning:**
- Chronic cough with hemoptysis raises concern for a lung malignancy.
- Persistent chest pain and unexplained weight loss are warning signs for cancer.
- Fatigue and weakness are common in chronic illnesses like cancer.
- Hoarseness can result from recurrent laryngeal nerve involvement by a lung tumor.
- These symptoms are indicative of a pulmonary neoplasm.

""",
'SLE':"""
Sex: Female, Age: 32
- I feel very tired and have pain in my joints.
- I have a rash on my face that looks like a butterfly.
- I feel chest pain when I take a deep breath.
- My hands feel cold and turn blue or white in the cold.
- I sometimes have a fever and hair loss.
- I feel stiff in the morning, especially in my fingers and knees.
- On a scale of 0-10, my joint pain is 6
- On a scale of 0-10, my fatigue is 7
- The affected regions are:
  * face
  * joints
  * chest

**Reasoning:**
- Butterfly-shaped facial rash is characteristic of systemic lupus erythematosus (SLE).
- Joint pain and morning stiffness indicate inflammatory arthritis common in SLE.
- Raynaud's phenomenon (hands turning blue or white in cold) is associated with SLE.
- Chest pain on deep breathing suggests pleuritis, a known manifestation of SLE.
- Fatigue, fever, and hair loss are systemic symptoms of SLE.

""",
'Sarcoidosis':"""
Sex: Male, Age: 40
- I have a persistent cough.
- I feel short of breath during physical activity.
- My eyes feel dry and irritated.
- I noticed red, raised patches on my skin.
- I feel very tired and weak.
- I have mild chest pain and discomfort.
- On a scale of 0-10, my fatigue is 7
- On a scale of 0-10, my chest discomfort is 5
- The affected regions are:
  * lungs
  * skin
  * eyes

**Reasoning:**
- Persistent cough and shortness of breath suggest pulmonary involvement.
- Skin lesions (red, raised patches) are common in sarcoidosis (erythema nodosum).
- Eye symptoms indicate possible uveitis associated with sarcoidosis.
- Fatigue and weakness are systemic symptoms.
- These multi-systemic symptoms point towards sarcoidosis.

""",
'Scombroid food poisoning':"""
Sex: Male, Age: 34
- I ate fish that tasted strange before these symptoms started.
- I feel flushed and hot.
- I have a rash on my skin.
- My heart feels like it's racing.
- I feel nauseous and have diarrhea.
- I have a headache and abdominal cramps.
- On a scale of 0-10, my nausea is 6
- On a scale of 0-10, my abdominal cramps are 7
- The affected regions are:
  * skin
  * abdomen

**Reasoning:**
- Consumption of fish that tasted strange suggests possible histamine (scombroid) poisoning.
- Flushing, rash, and tachycardia are symptoms of histamine release.
- Gastrointestinal symptoms like nausea, diarrhea, and abdominal cramps are common.
- Rapid onset after eating fish supports scombroid poisoning.
- These symptoms align with scombroid food poisoning.

""",
'Spontaneous pneumothorax':"""
Sex: Male, Age: 22
- I feel sudden and sharp chest pain.
- I feel short of breath.
- My breathing feels faster and shallower than normal.
- I feel lightheaded and dizzy.
- My chest feels tight on one side.
- I have a dry cough.
- On a scale of 0-10, my chest pain is 8
- On a scale of 0-10, my difficulty breathing is 7
- The affected regions are:
  * chest (right)
  * lungs

**Reasoning:**
- Sudden onset of unilateral chest pain and shortness of breath suggests pneumothorax.
- Young males are at higher risk for spontaneous pneumothorax.
- Decreased breath sounds and chest tightness on one side support this.
- Lightheadedness may result from decreased oxygenation.
- These findings are consistent with a spontaneous pneumothorax.

""",
'Spontaneous rib fracture':"""
Sex: Female, Age: 67
- I feel sudden pain in my chest or back without an injury.
- The pain worsens when I take a deep breath or move.
- I feel tenderness when I press on my ribs.
- I feel short of breath during activity.
- I sometimes hear a popping or cracking sound.
- On a scale of 0-10, my chest pain is 7
- On a scale of 0-10, my discomfort is 6
- The affected regions are:
  * chest
  * back
  * ribs

**Reasoning:**
- Sudden rib pain without trauma suggests possible pathological fracture.
- Osteoporosis in older females increases risk for spontaneous fractures.
- Pain worsening with breathing or movement is typical of rib fractures.
- Tenderness over the ribs supports a fracture.
- These symptoms point toward a spontaneous rib fracture.

""",
'Stable angina':"""
Sex: Male, Age: 55
- I feel chest pain when I exercise or climb stairs.
- The pain goes away when I rest.
- The pain feels like pressure or squeezing.
- I feel short of breath during the pain.
- The pain sometimes spreads to my left arm or jaw.
- I feel fatigued after the episodes.
- On a scale of 0-10, my chest pain is 6
- On a scale of 0-10, my fatigue is 4
- The affected regions are:
  * chest
  * left arm
  * jaw

**Reasoning:**
- Chest pain induced by exertion and relieved by rest is characteristic of stable angina.
- Pain described as pressure or squeezing supports cardiac ischemia.
- Radiation to the left arm or jaw is typical of angina.
- Shortness of breath during pain indicates myocardial oxygen demand exceeding supply.
- These symptoms are consistent with stable angina pectoris.

""",
'Tuberculosis':"""
Sex: Female, Age: 45
- I have a persistent cough that produces yellow or bloody mucus.
- I have a fever and night sweats.
- I have lost weight without trying.
- I feel fatigued and weak.
- I sometimes feel chest pain when I cough.
- I have noticed swollen lymph nodes in my neck.
- On a scale of 0-10, my cough intensity is 7
- On a scale of 0-10, my fatigue is 8
- The affected regions are:
  * lungs
  * chest
  * neck

**Reasoning:**
- Chronic productive cough with hemoptysis suggests pulmonary TB.
- Fever, night sweats, and weight loss are classic symptoms of tuberculosis.
- Chest pain during coughing indicates lung involvement.
- Swollen cervical lymph nodes can occur in TB (scrofula).
- These findings are indicative of tuberculosis infection.

""",
'URTI':"""
Sex: Female, Age: 32
- I have a sore throat and runny nose.
- I am sneezing frequently.
- I have a mild fever.
- My voice feels hoarse.
- I feel tired but can still go about my day.
- My cough is dry and irritating.
- On a scale of 0-10, my throat pain is 5
- On a scale of 0-10, my fatigue is 4
- The affected regions are:
  * throat
  * nose
  * chest

**Reasoning:**
- Symptoms like sore throat, runny nose, sneezing, and mild fever suggest a common cold.
- Dry, irritating cough and hoarseness are typical of URTIs.
- Ability to continue daily activities indicates a mild infection.
- These symptoms are consistent with an upper respiratory tract infection.

""",
'Unstable angina':"""
Sex: Male, Age: 60
- I feel chest pain even when I am resting.
- The pain feels like pressure or squeezing.
- I feel short of breath during the pain.
- The pain spreads to my arms and jaw.
- The pain lasts longer than 15 minutes.
- I feel nauseous and sweaty during the pain.
- On a scale of 0-10, my chest pain is 8
- On a scale of 0-10, my nausea is 5
- The affected regions are:
  * chest
  * arms
  * jaw

**Reasoning:**
- Chest pain at rest indicates unstable angina, a sign of worsening cardiac ischemia.
- Pain lasting longer than 15 minutes is concerning for acute coronary syndrome.
- Associated symptoms like nausea and sweating support cardiac origin.
- Radiation of pain to arms and jaw is typical.
- These symptoms suggest unstable angina, requiring immediate attention.

""",
'Viral pharyngitis':"""
Sex: Female, Age: 20
- I have a sore throat that started suddenly.
- My throat feels scratchy and dry.
- I have a mild fever.
- My voice feels hoarse.
- I have a headache and body aches.
- I feel tired and weak.
- On a scale of 0-10, my throat pain is 6
- On a scale of 0-10, my fatigue is 5
- The affected regions are:
  * throat
  * head
  * body

**Reasoning:**
- Sudden onset of sore throat with scratchiness suggests viral infection.
- Mild fever, headache, and body aches are common in viral illnesses.
- Hoarseness indicates laryngeal involvement.
- Fatigue and weakness further support a viral etiology.
- These symptoms are consistent with viral pharyngitis.

""",
'Whooping cough':"""
Sex: Male, Age: 3
- I have severe coughing fits that make it hard to breathe.
- I make a whooping sound when I breathe in after coughing.
- I sometimes vomit after coughing.
- I have a low-grade fever.
- My nose is runny.
- I feel very tired after coughing fits.
- On a scale of 0-10, my coughing intensity is 8
- On a scale of 0-10, my fatigue is 7
- The affected regions are:
  * chest
  * throat

**Reasoning:**
- Severe coughing fits with a whooping sound are classic for pertussis (whooping cough).
- Post-cough vomiting is common in children with pertussis.
- Runny nose and low-grade fever are initial symptoms.
- Fatigue after coughing fits indicates the severity of episodes.
- These findings are characteristic of whooping cough.

"""
}

def get_medical_record():
    return medical_records
def gen_shot(i, key, value):
    return f"""
patient profile:
{value}
**Answer:**
{i}. {key}
"""
# for i, (key, value) in enumerate(medical_records.items()):
#     # print(gen_shot(i, key, value))
#     profile = re.search(r"^.*?(?=\*\*Reasoning:\*\*)", value, re.DOTALL).group().strip()
#     try:
#       reasoning = re.search(r"(?<=\*\*Reasoning:\*\*).+?(?=\*\*Answer:\*\*)", gen_shot(i, key, value), re.DOTALL).group().strip()
#     except:
#       try:
#         reasoning = re.search(r"(?<=\*\*Reasoning:\*\*).+", gen_shot(i, key, value), re.DOTALL).group().strip()
#       except:
#         reasoning = ""
#     try:
#       ans = re.search(r"(?<=\*\*Answer:\*\*).+", gen_shot(i, key, value), re.DOTALL).group().strip()
#       numbers = re.findall(pattern=r"(\d+)\.", string=ans)
#     except:
#       ans = ""
#       numbers = re.findall(pattern=r"(\d+)\.", string=gen_shot(i, key, value))
#     if i == 0:
# #         str = f"""
# # patient file:
# # Sex: Male, Age: 3
# # - I have severe coughing fits that make it hard to breathe.
# # - I make a whooping sound when I breathe in after coughing.
# # - I sometimes vomit after coughing.
# # - I have a low-grade fever.
# # - My nose is runny.
# # - I feel very tired after coughing fits.
# # - On a scale of 0-10, my coughing intensity is 8
# # - On a scale of 0-10, my fatigue is 7
# # - The affected regions are:
# # * chest
# # * throat

# # **Reasoning:**
# # {reasoning}

# # **Answer:**
# # {numbers[0]}
# #         """
#         print(reasoning)