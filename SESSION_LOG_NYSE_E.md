# Session Log — NYSE Letter E

**Method**: v4 text-based extraction (tipranks widget `get_page_text` for Low/Avg/High, eToro `/research` page `get_page_text` for price + `javascript_exec` for tradeability). See `NYSE_PROJECT_LOG.md` and `PROJECT_LOG.md`'s v4 method section.

**Tickers**: 87, sourced from `grep '^E' nyse_data.tsv`, sorted. Full list:
E EAF EAT EBF EBS EC ECG ECL ECVT ED EDN EDU EE EFC EFOR EFR EFX EFXT EG EGHT EGO EGP.US EGY EHC EIG EIX EL ELAN ELF ELME ELPC ELS ELV EMA EMBJ EME EMN EMR ENB ENIC ENOV ENR ENS.US ENVA EOG EPAC EPAM EPC EPD EPM EPR EPRT EQBK EQH EQNR EQT EQX ERO EROC EROK ES ESAB ESE ESI ESNT ESRT ESS ESTC ET ETD ETN ETR ETSY EVC EVEX EVH EVI EVR EVRG EVTC EVVAQ EW EXE EXK EXP EXPD EXR

**Progress**: 87/87 DONE. Completed 2026-08-27, same session as C2/D. No blocks the entire letter. Completeness audit passed (87/87, both directions, no duplicates). NOFAQ: EBF, EDN, EFR, ELME, ELPC, EVC, EVI (7). NOT_TRADEABLE: EVVAQ (Enviva Inc, bankrupt shell, price $0.0001 — confirmed via disabled Trade button rather than treated as CVR since it's not a merger CVR case). All others OK/TRADEABLE.
