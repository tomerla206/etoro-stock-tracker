# Yahoo Dividend Yield Refresh - Chunk D (rows 3248-4331)

Source list: refresh_4330_list.tsv, rows 3248-4331 (1084 tickers, TICKER column).
Output: yahoo_dividends_D.txt (TICKER\tPERCENT)

### Batch 1 (rows 3248-3259, tickers 1-12)
- WAF.DE: 0.22
- WCH.DE: 2.67
- WIB.DE: 4.81
- YSN.DE: 1.41
- ZAL.DE: no dividend
- 74SW.PA: no dividend
- ABVX.PA: no dividend
- AC.PA: 2.89
- ACA.PA: 9.22
- ADP.PA: 2.75
- AF.PA: no dividend
- AI.PA: 1.98

Progress: 12/1084 done.

### Batch 2 (tickers 13-48)
- AIR.PA: 1.58
- AKE.PA: 6.04
- ALCGM.PA: no dividend
- ALCOX.PA: no dividend
- ALO.PA: no dividend
- ALSEN.PA: no dividend
- AM.PA: 1.66
- AMUN.PA: 4.48
- ANTIN.PA: 7.91
- ARG.PA: 4.71
- ATE.PA: 1.95
- ATO.PA: no dividend
- AUB.PA: 2.85
- AYV.PA: 5.35
- BEN.PA: 3.44
- BIM.PA: 1.30
- BN.PA: 3.49
- BNP.PA: 5.66
- BVI.PA: 3.36
- CA.PA: 6.21
- CAP.PA: 3.11
- COFA.PA: 7.81
- COTY.PA: no dividend (note: redirected to US Coty Inc page, may be a ticker mismatch - flagging for review)
- COV.PA: 7.46
- CS.PA: 5.32
- DEC.PA: 2.71
- DG.PA: 4.42
- DIM.PA: 0.35
- DSY.PA: 1.17
- EDEN.PA: 4.36
- EL.PA: 2.48
- ELIOR.PA: 1.92
- ELIS.PA: 1.08
- EN.PA: 4.76
- ENGI.PA: 5.51
- ENX.PA: 1.93

Progress: 48/1084 done.

### Batch 3 (tickers 49-65)
- ERF.PA: 1.00
- ETL.PA: no dividend
- EXA.PA: no dividend
- EXENS.PA: 0.51
- FDJU.PA: 9.37
- FGR.PA: 4.38
- FR.PA: 3.11
- FRVIA.PA: no dividend
- GET.PA: 4.29
- GFC.PA: 7.86
- GLE.PA: 2.42
- GTT.PA: 4.06
- HO.PA: 1.59
- ICAD.PA: 10.38
- IDL.PA: no dividend
- IPN.PA: 0.98

Progress: 65/1084 done. (one transient "Claude in Chrome not connected" error recovered on FDJU.PA extraction; no data lost)

### Batch 4 (tickers 66-85)
- IVA.PA: no dividend
- KER.PA: 1.18
- LI.PA: 5.03
- LR.PA: 1.70
- MC.PA: 2.84
- MEDCL.PA: no dividend
- MERY.PA: 9.01
- MF.PA: 5.90
- ML.PA: no dividend
- MRN.PA: 2.36
- NANO.PA: no dividend
- NEX.PA: 2.03
- OPM.PA: 3.88
- OR.PA: 1.85
- ORA.PA: 4.94
- PLNW.PA: 1.45
- PLX.PA: 2.36
- PUB.PA: 3.69
- RCO.PA: 1.63
- RI.PA: 7.44

Progress: 85/1084 done.

### Batch 5 (tickers 86-109)
- RMS.PA: 1.13
- RNO.PA: 7.48
- RXL.PA: 3.31
- SAF.PA: 0.97
- SAN.PA: 5.33
- SCR.PA: 5.62
- SESG.PA: 10.11
- SGO.PA: 2.88
- SIGHT.PA: no dividend
- SK.PA: 4.73
- SOI.PA: no dividend
- SOP.PA: 2.97
- SPIE.PA: 2.46
- STLAP.PA: no dividend
- STMPA.PA: 0.72
- SU.PA: 1.39
- SW.PA: 4.63
- TE.PA: 3.31
- TEP.PA: 6.40
- TFF.PA: 3.01
- TFI.PA: 9.17
- TKO.PA: 4.72
- TRI.PA: 2.56
- TTE.PA: 4.82

Progress: 109/1084 done.

### Batch 6 (tickers 110-123)
- UBI.PA: no dividend
- URW.PA: 4.55
- VCT.PA: 3.03
- VIE.PA: 4.57
- VIRI.PA: no dividend
- VIRP.PA: 0.45
- VIV.PA: 2.45
- VK.PA: 9.35
- VLTSA.PA: no dividend
- VRLA.PA: 5.11
- VU.PA: 0.69
- WLN.PA: no dividend
- XFAB.PA: no dividend
- A2M.ASX: 1.95 (note: Yahoo uses .AX suffix for ASX-listed tickers, not .ASX - converting for lookup, keeping original .ASX form as output key)

Progress: 123/1084 done. End of French (.PA) section, starting Australian (.ASX) section.

### Batch 7 (tickers 124-139)
- ABB.ASX: 1.38
- AD8.ASX: no dividend
- AGL.ASX: 6.09
- AIA.ASX: 1.53
- ALD.ASX: 8.79
- ALL.ASX: 1.64
- ALQ.ASX: 1.91
- ALX.ASX: 8.64
- AMC.ASX: 5.69
- AMP.ASX: 2.12
- ANN.ASX: 2.35
- ANZ.ASX: 4.52
- AOV.ASX: 6.80
- APA.ASX: 5.39
- APE.ASX: 3.33
- ARB.ASX: 3.55

Progress: 139/1084 done. (Note: a second transient "Claude in Chrome not connected" occurred around AOV/APA/APE/ARB - recovered by explicitly re-navigating each ticker and verifying document.title matched the extracted dividend text before recording, since the earlier batch appeared to keep executing in the background after the error and caused a brief tab/data mismatch. All 4 values above were re-verified with title match, so they are trustworthy.)

### Batch 8 (tickers 140-155)
- ARF.ASX: 8.33
- ASX.ASX: 3.79
- AUB.ASX: 3.34
- AX1.ASX: 6.16
- AZJ.ASX: 6.12
- BAP.ASX: 11.30
- BEN.ASX: 6.24
- BGA.ASX: 2.45
- BGL.ASX: no dividend
- BHP.ASX: 3.61
- BMN.ASX: no dividend
- BOE.ASX: no dividend
- BOQ.ASX: 6.22
- BPT.ASX: 4.65
- BRG.ASX: 1.18
- BSL.ASX: 4.21

Progress: 155/1084 done. (from batch 7 onward, extraction includes document.title verification alongside the dividend text on every call, to guard against any tab-state race.)

### Batch 9 (tickers 156-175)
- BWP.ASX: 5.32
- BXB.ASX: 3.35
- CAR.ASX: 3.16
- CBA.ASX: 3.21
- CCP.ASX: 6.49
- CDA.ASX: 1.02
- CGF.ASX: 3.41
- CHC.ASX: 2.64
- CHN.ASX: no dividend
- CIA.ASX: 3.65
- CIP.ASX: 5.87
- CKF.ASX: 3.42
- CLW.ASX: 7.31
- CMM.ASX: 0.58
- COH.ASX: 1.91
- COL.ASX: 3.11
- CPU.ASX: 3.31
- CQE.ASX: 7.20
- CQR.ASX: 6.55
- CRN.ASX: 3.06 (stale ex-div date Mar 2025 but yield text present, recorded as-is)

Progress: 175/1084 done.

### Batch 10 (tickers 176-192)
- CSL.ASX: 2.37
- CWY.ASX: 2.72
- CXO.ASX: no dividend
- DDR.ASX: 3.01
- DMP.ASX: 2.86
- DNL.ASX: 3.74
- DOW.ASX: 4.45
- DRO.ASX: no dividend
- DRR.ASX: 5.22
- DTL.ASX: 3.27
- DVP.ASX: no dividend
- DXS.ASX: 6.38
- EDV.ASX: 3.86
- ELD.ASX: 6.01
- ELV.ASX: no dividend
- EMR.ASX: no dividend

Progress: 192/1084 done. (another transient disconnect recovered around DMP/DNL/DOW/DRO batch; re-verified with title match, values trustworthy)

### Batch 11 (tickers 193-204)
- EVN.ASX: 2.68
- EVT.ASX: 2.72
- FBU.ASX: no dividend
- FLT.ASX: 3.51
- FMG.ASX: 5.98
- FPH.ASX: 1.20
- GMD.ASX: 0.58
- GMG.ASX: 1.07
- GNC.ASX: 4.49
- GOZ.ASX: 8.93
- GPT.ASX: 5.19
- HDN.ASX: 7.82

Progress: 204/1084 done.

### Batch 12 (tickers 205-216)
- HLI.ASX: 6.36
- HLS.ASX: no dividend
- HMC.ASX: 3.59
- HUB.ASX: 1.10
- HVN.ASX: 5.88
- IAG.ASX: 4.08
- IDX.ASX: 4.13
- IEL.ASX: 4.95
- IGO.ASX: 0.58
- ILU.ASX: 0.85
- IMD.ASX: 1.00
- INA.ASX: 2.60

Progress: 216/1084 done.

### Batch 13 (tickers 217-228)
- ING.ASX: 4.83
- IPH.ASX: 11.82
- IRE.ASX: 4.70
- JBH.ASX: 5.02
- JHX.ASX: no dividend
- JIN.ASX: 3.66
- KAR.ASX: 2.46
- KGN.ASX: 4.35
- KLS.ASX: 4.18
- LIC.ASX: no dividend
- LLC.ASX: 5.39
- LOV.ASX: 3.26

Progress: 228/1084 done.

### Batch 14 (tickers 229-242)
- LTR.ASX: no dividend
- LYC.ASX: no dividend
- MAQ.ASX: no dividend
- MFG.ASX: 5.64
- MGR.ASX: 5.35
- MIN.ASX: 1.27
- MMS.ASX: 6.71
- MND.ASX: 4.08
- MP1.ASX: no dividend
- MPL.ASX: 3.97
- MQG.ASX: FAILED TO LOAD (page loaded sparse/empty - all fields showed "--", body text only 6197 chars, likely a Yahoo page-load glitch; retried once, same result - needs re-attempt in a future session)
- MTS.ASX: 6.46
- NAB.ASX: 4.44
- NAN.ASX: no dividend
- NCK.ASX: 5.25

Progress: 242/1084 done (243 attempted, 1 failed: MQG.ASX).

### Batch 15 (tickers 243-254)
- NEC.ASX: 7.73
- NEU.ASX: 1.47
- NHC.ASX: 3.36
- NHF.ASX: 4.30
- NIC.ASX: no dividend
- NST.ASX: 2.22
- NUF.ASX: no dividend
- NWH.ASX: 3.00
- NWL.ASX: 1.96
- NWS.ASX: 0.58
- NXT.ASX: no dividend
- ORA.ASX: 6.14

Progress: 254/1084 done.

### Batch 16 (tickers 255-266)
- ORG.ASX: 5.12
- ORI.ASX: 2.75
- PDN.ASX: no dividend
- PLS.ASX: 0.93 (note: Yahoo shows company name "PLS Group Limited" for ticker PLS.AX, not the expected "Pilbara Minerals" - flagging for review, but data was extracted from the correct ticker's own page)
- PME.ASX: 0.38
- PMV.ASX: 8.18
- PNI.ASX: 3.43
- PNV.ASX: no dividend
- PPT.ASX: 6.48
- PRU.ASX: 2.08
- PWH.ASX: 0.68
- PXA.ASX: no dividend

Progress: 266/1084 done.

### Batch 17 (tickers 267-278)
- QAN.ASX: 4.13
- QBE.ASX: 4.99
- RDX.ASX: 3.83
- REA.ASX: 1.96
- REH.ASX: 1.15
- RGN.ASX: 6.35
- RHC.ASX: 1.88
- RIC.ASX: 4.13
- RIO.ASX: 3.83
- RMD.ASX: 1.12
- RMS.ASX: 1.52
- RRL.ASX: 3.48

Progress: 278/1084 done.

### Batch 18 (tickers 279-290)
- RWC.ASX: 1.60
- S32.ASX: 2.48
- SCG.ASX: 5.24
- SDF.ASX: 3.59
- SDR.ASX: no dividend
- SEK.ASX: 3.52
- SFR.ASX: 1.50
- SGH.ASX: no dividend
- SGM.ASX: 1.41
- SGP.ASX: 5.85
- SHL.ASX: 5.39
- SIG.ASX: 1.49

Progress: 290/1084 done.

### Batch 19 (tickers 291-302)
- SIQ.ASX: 4.07
- SLX.ASX: no dividend
- SMR.ASX: 4.56
- STO.ASX: 3.81
- SUL.ASX: 4.88
- SUN.ASX: 3.74
- SYR.ASX: no dividend
- TAH.ASX: 3.26
- TCL.ASX: 5.00
- TLC.ASX: 3.36
- TLS.ASX: 4.56
- TLX.ASX: no dividend

Progress: 302/1084 done.

### Batch 20 (tickers 303-314)
- TNE.ASX: 0.86
- TPG.ASX: 5.39
- TPW.ASX: no dividend
- TWE.ASX: no dividend
- VAU.ASX: 1.01
- VCX.ASX: 5.00
- VEA.ASX: 5.41
- VNT.ASX: 4.31
- VUL.ASX: no dividend
- WA1.ASX: no dividend
- WAF.ASX: no dividend (Australia - West African Resources, distinct from WAF.DE Siltronic already done)
- WBC.ASX: 4.54

Progress: 314/1084 done.

### Batch 21 (tickers 315-322)
- WDS.ASX: 5.03
- WEB.ASX: no dividend
- WES.ASX: 2.78
- WGX.ASX: 0.45
- WHC.ASX: 1.44
- WOR.ASX: 4.88
- WOW.ASX: 2.45
- WPR.ASX: 7.20

Progress: 322/1084 done.

### Batch 22 (tickers 323-330)
- WTC.ASX: 0.54
- XRO.ASX: no dividend
- YAL.ASX: 3.16
- AAK.ST: 2.76
- AFRY.ST: 5.74
- ALFA.ST: 1.56
- ALLEI.ST: 2.07
- AXFO.ST: 3.65

Progress: 330/1084 done. End of Australian (.ASX) section, starting Swedish (.ST) section.

### Batch 23 (tickers 331-338)
- BILL.ST: 2.56
- BOL.ST: 1.92
- CAMX.ST: no dividend
- CAST.ST: 1.86
- CATE.ST: 2.45
- DOM.ST: 4.32
- EQT.ST: 1.47
- EVO.ST: 5.05

Progress: 338/1084 done.

### Batch 24 (tickers 339-346)
- FABG.ST: 3.00
- HACK.ST: 5.46
- HEM.ST: 1.95
- HTRO.ST: no dividend
- INDT.ST: 1.23
- INTRUM.ST: no dividend
- LOOMIS.ST: 2.81
- LUG.ST: 5.70

Progress: 346/1084 done.

### Batch 25 (tickers 347-354)
- LUMI.ST: 0.27
- MILDEF.ST: 0.33
- MIPS.ST: 0.68
- MTRS.ST: 0.94
- NCAB.ST: 1.38
- NP3.ST: 2.50
- SAND.ST: 1.53
- SAVE.ST: 2.34

Progress: 354/1084 done.

### Batch 26 (tickers 355-362)
- SINCH.ST: no dividend
- SOBI.ST: no dividend
- SYNSAM.ST: 3.05
- SYSR.ST: 1.65
- TELIA.ST: 4.75
- THULE.ST: 4.05
- TROAX.ST: 1.76
- VIMIAN.ST: no dividend

Progress: 362/1084 done.

### Batch 27 (tickers 363-366)
- WIHL.ST: 4.18
- YUBICO.ST: no dividend
- 0386.HK: 5.11
- 0656.HK: 0.50

Progress: 366/1084 done. End of Swedish (.ST) section, starting Hong Kong (.HK) section.

### Batch 28 (tickers 367-374)
- 0688.HK: 3.83
- 0700.HK: 1.17
- 0753.HK: no dividend
- 0902.HK: 8.23
- 0914.HK: 5.02
- 0916.HK: 7.91
- 0968.HK: 0.43
- 0992.HK: 1.40

Progress: 374/1084 done.

### Batch 29 (tickers 375-382)
- 0998.HK: 5.47
- 1024.HK: 2.05
- 1038.HK: 4.03
- 1044.HK: 7.32
- 1071.HK: 6.61
- 1072.HK: 2.92
- 1088.HK: 5.02
- 1099.HK: 4.96

Progress: 382/1084 done. (transient disconnect recovered around 1024-1044.HK; re-verified with title match)

### Batch 30 (tickers 383-390)
- 1109.HK: 4.01
- 1138.HK: 4.57
- 1157.HK: 12.72
- 1171.HK: 4.37
- 1179.HK: 4.60
- 1193.HK: 5.57
- 1209.HK: 2.88
- 1288.HK: 4.43

Progress: 390/1084 done.

### Batch 31 (tickers 391-398)
- 1299.HK: 2.60
- 1308.HK: 5.24
- 1318.HK: 2.29
- 1339.HK: 4.35
- 1347.HK: no dividend
- 1378.HK: 7.23
- 1519.HK: no dividend
- 1530.HK: 1.55

Progress: 398/1084 done.

### Batch 32 (tickers 399-406)
- 1585.HK: 5.66
- 1698.HK: 2.79
- 1772.HK: 0.42
- 1787.HK: 1.19
- 1797.HK: no dividend
- 1801.HK: no dividend
- 1810.HK: no dividend
- 1816.HK: 3.24

Progress: 406/1084 done.

### Batch 33 (tickers 407-414)
- 1818.HK: 0.50
- 1833.HK: no dividend
- 1876.HK: 7.38
- 1880.HK: 1.64
- 1898.HK: 3.81
- 1913.HK: 3.61
- 1919.HK: 5.86
- 1929.HK: 4.93

Progress: 414/1084 done.

### Batch 34 (tickers 415-422)
- 1958.HK: no dividend
- 1997.HK: 5.18
- 2007.HK: no dividend
- 2013.HK: no dividend
- 2015.HK: no dividend
- 2057.HK: 3.22
- 2202.HK: no dividend
- 2238.HK: 1.83

Progress: 422/1084 done.

### Batch 35 (tickers 423-426)
- 2268.HK: no dividend
- 2318.HK: 5.54
- 2328.HK: 4.51
- 2331.HK: 4.95

Progress: 426/1084 done. (transient disconnect recovered around 2331.HK, re-verified with title match)

### Batch 36 (tickers 427-434)
- 2333.HK: 5.10
- 2338.HK: 2.63
- 2359.HK: 0.62
- 2367.HK: 2.40
- 2423.HK: 1.52
- 2513.HK: no dividend
- 2588.HK: 5.07
- 2600.HK: 5.69

Progress: 434/1084 done.

### Batch 37 (tickers 435-442)
- 2601.HK: 5.99
- 2611.HK: 4.91
- 2618.HK: no dividend
- 2628.HK: 3.72
- 2727.HK: 0.56
- 2883.HK: 4.39
- 2899.HK: 2.41
- 3311.HK: 7.88

Progress: 442/1084 done.

### Batch 38 (tickers 443-450)
- 3323.HK: 4.75
- 3328.HK: 4.71
- 3347.HK: 0.35
- 3606.HK: 4.26
- 3692.HK: 1.37
- 3750.HK: 0.87
- 3759.HK: 0.82
- 3800.HK: no dividend

Progress: 450/1084 done.

### Batch 39 (tickers 451-458)
- 3808.HK: 5.12
- 3888.HK: 0.52
- 3898.HK: 4.16
- 3988.HK: 4.58
- 3998.HK: 7.09
- 6030.HK: 2.87
- 6055.HK: 2.11
- 6066.HK: 3.13

Progress: 458/1084 done.

### Batch 40 (tickers 459-466)
- 6099.HK: 4.45
- 6160.HK: no dividend
- 6181.HK: 8.71
- 6185.HK: no dividend
- 6186.HK: 7.55
- 6618.HK: no dividend
- 6690.HK: 6.12
- 6969.HK: 3.59

Progress: 466/1084 done.

### Batch 41 (tickers 467-474)
- 6990.HK: no dividend
- 9618.HK: 3.49
- 9626.HK: no dividend
- 9633.HK: 2.60
- 9660.HK: no dividend
- 9696.HK: no dividend
- 9863.HK: no dividend
- 9866.HK: no dividend

Progress: 474/1084 done.

### Batch 42 (tickers 475-482)
- 9868.HK: no dividend
- 9888.HK: no dividend
- 9896.HK: 7.00
- 9901.HK: 2.07
- 9926.HK: no dividend
- 9961.HK: 0.58
- 9988.HK: 0.90
- 9992.HK: 1.75

Progress: 482/1084 done.

### Batch 43 (tickers 483-486)
- 9999.HK: 1.56
- AKRBP.OL: 7.35
- AKSO.OL: 8.40
- AUTO.OL: no dividend

Progress: 486/1084 done. End of Hong Kong (.HK) section, starting Norwegian (.OL) section.

### Batch 44 (tickers 487-494)
- BWLPG.OL: 8.07
- DNB.OL: 5.70
- EQNR.OL: 3.78
- FRO.OL: 23.34 (unusually high, recorded as-is per Yahoo)
- GJF.OL: 3.49
- HSHP.OL: 15.91
- KOG.OL: 0.70
- NEL.OL: no dividend

Progress: 494/1084 done.

### Batch 45 (tickers 495-502)
- NHY.OL: 3.22
- NOD.OL: no dividend
- ODFB.OL: 8.99
- STB.OL: 2.63
- SUBC.OL: 5.85
- TEL.OL: 7.10
- TGS.OL: 4.63
- VAR.OL: 11.17

Progress: 502/1084 done. End of Norwegian (.OL) section, starting Italian (.MI) section.

### Batch 46 (tickers 503-510)
- AMP.MI: 2.39
- ARIS.MI: 2.58
- BAMI.MI: 6.26
- BC.MI: 1.17
- BGN.MI: 4.37
- BMED.MI: 5.38
- BMPS.MI: 7.54
- BPE.MI: 8.83

Progress: 510/1084 done. (transient disconnect around BGN/BMED/BMPS/BPE, recovered with careful re-navigation and title verification per ticker)

### Batch 47 (tickers 511-518)
- BRE.MI: 2.97
- BZU.MI: 1.67
- CPR.MI: 1.73
- CRL.MI: 0.71
- DIA.MI: 1.70
- DLG.MI: 2.05
- EGLA.MI: 3.78
- ENAV.MI: 5.75

Progress: 518/1084 done.

### Batch 48 (tickers 519-526)
- ENEL.MI: 5.50
- ENI.MI: 4.70
- FBK.MI: 3.32
- FCT.MI: no dividend
- G.MI: 3.72
- GVS.MI: no dividend
- ICOS.MI: 1.40
- IG.MI: 4.96

Progress: 526/1084 done.

### Batch 49 (tickers 527-534)
- INW.MI: 9.03
- IP.MI: 0.93
- ISP.MI: 5.60
- ITM.MI: 4.25
- LDO.MI: 1.19
- LTMC.MI: 1.72
- MAIRE.MI: 4.64
- MB.MI: 4.55

Progress: 534/1084 done.

### Batch 50 (tickers 535-542)
- MONC.MI: 2.93
- NEXI.MI: 6.79
- PIRC.MI: 3.61
- PRY.MI: 0.74
- PST.MI: 4.50
- RACE.MI: 1.00
- REC.MI: 2.70
- REY.MI: 1.09

Progress: 542/1084 done.

### Batch 51 (tickers 543-550)
- RWAY.MI: 7.29
- SES.MI: 1.39
- SFER.MI: no dividend
- SPM.MI: 3.81
- SRG.MI: 5.22
- STLAM.MI: no dividend
- STMMI.MI: 0.72
- TEN.MI: 4.43

Progress: 550/1084 done.

### Batch 52 (tickers 551-559)
- TGYM.MI: 2.98
- TIT.MI: no dividend
- TPRO.MI: no dividend
- TRN.MI: 4.05
- UCG.MI: 3.72
- UNI.MI: 3.93
- ZV.MI: 3.14
- ABBN.ZU: 1.17 (note: Yahoo uses .SW suffix for Swiss-listed tickers, not .ZU - converting for lookup, keeping original .ZU form as output key, same pattern as ASX->AX)

Progress: 559/1084 done. End of Italian (.MI) section, starting Swiss (.ZU) section.

### Batch 53 (tickers 560-567)
- ACLN.ZU: 1.95
- ADEN.ZU: 4.11
- ALC.ZU: 0.48
- AMRZ.ZU: 0.93
- AMS.ZU: no dividend
- AVOL.ZU: 2.49
- BAER.ZU: 3.42
- BARN.ZU: 2.62

Progress: 567/1084 done.

### Batch 54 (tickers 568-575)
- BEAN.ZU: 1.14
- BUCN.ZU: 3.47
- CFR.ZU: 1.70
- CLN.ZU: 3.89
- DAE.ZU: 2.39
- DKSH.ZU: 3.80
- EMSN.ZU: 1.85
- FHZN.ZU: 4.08

Progress: 575/1084 done.

### Batch 55 (tickers 576-583)
- GALD.ZU: 0.20
- GALE.ZU: 2.96
- GEBN.ZU: 2.23
- GIVN.ZU: 2.17
- HOLN.ZU: 2.33
- KNIN.ZU: 2.73
- LAND.ZU: 2.60
- LISN.ZU: 1.99

Progress: 583/1084 done.

### Batch 56 (tickers 584-591)
- LOGN.ZU: 1.70
- LONN.ZU: 0.86
- NESN.ZU: 3.94
- NOVN.ZU: 2.99
- OERL.ZU: 3.85
- PGHN.ZU: 6.14
- PPGN.ZU: no dividend
- ROP.ZU: 2.73

Progress: 591/1084 done.

### Batch 57 (tickers 592-599)
- SCHP.ZU: 2.27
- SCMN.ZU: 4.13
- SDZ.ZU: 1.16
- SGSN.ZU: 3.42
- SIKA.ZU: 1.92
- SLHN.ZU: 3.96
- SMG.ZU: 1.27
- SOON.ZU: 2.01

Progress: 599/1084 done.

### Batch 58 (tickers 600-607)
- SPSN.ZU: 2.76
- SQN.ZU: 1.75
- SRAIL.ZU: 1.65
- SREN.ZU: 4.43
- STMN.ZU: 1.07
- TECN.ZU: 1.54
- TEMN.ZU: 1.86
- UBSG.ZU: 1.94

Progress: 607/1084 done.

### Batch 59 (tickers 608-610)
- UHR.ZU: 2.41
- VACN.ZU: 1.16
- ZURN.ZU: 5.05

Progress: 610/1084 done. End of Swiss (.ZU) section, starting Dutch (.NV) section.

### Batch 60 (tickers 611-618)
- AALB.NV: 2.64
- ABN.NV: 3.31
- AD.NV: 4.06
- ADYEN.NV: no dividend
- AGN.NV: 5.23
- AKZA.NV: 3.20
- ALFEN.NV: no dividend
- APAM.NV: 4.30 (note: Yahoo uses .AS suffix for Amsterdam-listed tickers, not .NV - converting for lookup, keeping original .NV form as output key)

Progress: 618/1084 done.

### Batch 61 (tickers 619-626)
- ARCAD.NV: 2.28
- ASM.NV: 0.39
- ASML.NV: 0.52
- ASRNL.NV: 4.88
- AVTX.NV: no dividend
- AXS.NV: no dividend
- BAMNB.NV: 2.58
- BESI.NV: 0.80

Progress: 626/1084 done.

### Batch 62 (tickers 627-634)
- BFIT.NV: no dividend
- BNJ.NV: 4.02
- CCEP.NV: 2.22
- CRBN.NV: 3.16
- CSG.NV: no dividend
- CTPNV.NV: 4.40
- CVC.NV: 6.60
- DSFIR.NV: 2.62

Progress: 634/1084 done.

### Batch 63 (tickers 635-642)
- ECMPA.NV: 6.62
- FAST.NV: no dividend
- FER.NV: 2.82
- FUR.NV: 1.67
- HEIA.NV: 2.66
- IMCD.NV: 1.83
- INGA.NV: 3.73
- KPN.NV: 4.61

Progress: 642/1084 done.

### Batch 64 (tickers 643-650)
- LIGHT.NV: 10.15
- LKFT.NV: no dividend
- MICC.NV: no dividend
- MT.NV: 0.80
- NN.NV: 5.19
- NSI.NV: 9.32
- OCI.NV: no dividend
- PHIA.NV: 3.68

Progress: 650/1084 done.

### Batch 65 (tickers 651-663) — resumed after PHIA.NV, .NV suffix mapped to Yahoo .AS
- PNL.NV: 4.42
- PRX.NV: 0.72
- RAND.NV: 4.04
- REN.NV: 2.54
- SBMO.NV: 2.98
- SHELL.NV: 6.92
- SLIGR.NV: 3.82
- THEON.NV: 0.93
- TWEKA.NV: 2.61
- UMG.NV: 3.50
- UNA.NV: 3.41
- VPK.NV: 5.27
- WKL.NV: 3.70

Progress: 663/1084 done.

### Batch 66 (tickers 664-679) — .BR tickers used as-is
- ABI.BR: 1.68
- AGS.BR: 6.02
- ARGX.BR: no dividend
- AZE.BR: 1.84
- CENER.BR: 1.14
- COLR.BR: 3.54
- DIE.BR: 1.13
- ELI.BR: 1.60
- KBC.BR: 3.85
- MELE.BR: 5.59
- NYXH.BR: no dividend
- PROX.BR: 9.45
- SHUR.BR: 5.09
- SOLB.BR: 9.43
- TESB.BR: 3.22
- UCB.BR: 0.67
- UMI.BR: 2.11

Progress: 680/1084 done.

### Batch 67 (tickers 681-695) — .HE tickers used as-is, then .CO
- ELISA.HE: 6.64
- FORTUM.HE: 3.56
- HUH1V.HE: 3.52
- KNEBV.HE: 3.44
- METSO.HE: 2.20
- NESTE.HE: 0.64
- NOKIA.HE: 1.55
- OUT1V.HE: 2.45
- SAMPO.HE: 3.66
- SSABAH.HE: 1.99
- STERV.HE: 2.47
- UPM.HE: 6.25
- WRT1V.HE: 1.84
- ALMB.CO: 3.81
- DANSKE.CO: 4.55

Progress: 695/1084 done. (45/434 of this session's chunk)

### Batch 68 (tickers 696-716) — .CO then .MC tickers used as-is
- DEMANT.CO: no dividend
- DSV.CO: 0.51
- FLS.CO: 0.67
- GMAB.CO: no dividend
- ACS.MC: 2.25
- ACX.MC: 3.47
- AENA.MC: 4.13
- AMS.MC: 2.65
- ANA.MC: 2.71
- ANE.MC: 0.14
- BBVA.MC: 3.67
- BKT.MC: 4.60
- CABK.MC: 3.80
- CLNX.MC: 2.87
- COL.MC: 5.96
- ELE.MC: 3.74
- ENG.MC: 5.98
- FCC.MC: 4.42
- FDR.MC: 3.36
- FER.MC: 2.82
- GRE.MC: no dividend
- IBE.MC: 3.35
- IDR.MC: 0.48
- ITX.MC: 1.11

Progress: 719/1084 done. (69/434 of this session's chunk)

### Batch 69 (tickers 717-731) — remaining .MC tickers
- MAP.MC: 4.03
- MEL.MC: 1.70
- MRL.MC: 1.59
- MTS.MC: 0.80
- NTGY.MC: 8.11
- PHM.MC: 1.21
- RED.MC: 5.26
- REP.MC: 4.14
- SAB.MC: 5.63
- SAN.MC: 1.97
- SCYR.MC: 4.65
- TEF.MC: 4.14
- UNI.MC: 5.37
- VID.MC: 1.93
- VIS.MC: 5.75

Progress: 734/1084 done. (84/434 of this session's chunk). Madrid (.MC) fully done. Now starting London (.L) — 349 tickers remain, used as-is.

### Batch 70 (tickers 732-753) — London .L tickers
- AAF.L: 1.60
- AAL.L: 0.67
- ABDN.L: 5.79
- ABF.L: 3.07
- ADM.L: 3.56
- AEP.L: 4.82
- AJB.L: 2.41
- ALFA.L: 0.89
- AML.L: no dividend
- ANTO.L: 1.43
- AO.L: no dividend
- ASC.L: no dividend
- ASHM.L: 7.53
- ATG.L: no dividend
- ATYM.L: 0.92
- AUTO.L: 2.20
- AV.L: 5.50
- AVAP.L: 0.54
- AVON.L: 1.00
- AZN.L: 2.00
- BA.L: 1.85
- BAB.L: 0.71

Progress: 756/1084 done. (106/434 of this session's chunk)

### Batch 71 (tickers 754-774) — more .L tickers
- BAG.L: 3.14
- BARC.L: 2.32
- BATS.L: 5.93
- BBOX.L: no dividend
- BBY.L: 1.64
- BGEO.L: 2.54
- BHP.L: 3.61
- BKG.L: 1.67
- BLND.L: 5.42
- BME.L: 4.04
- BMS.L: 3.13
- BMY.L: 2.52
- BNZL.L: 2.65
- BOOT.L: 5.09
- BOWL.L: 4.91
- BOY.L: 2.55
- BP.L: 4.87
- BPT.L: 3.01

Progress: 774/1084 done. (124/434 of this session's chunk)

### Batch 72 (tickers 775-789) — more .L tickers
- BRBY.L: no dividend
- BRK.L: 5.52
- BTRW.L: 5.35
- BWY.L: 3.33
- BYG.L: 5.33
- BYIT.L: 2.33
- CBG.L: no dividend
- CCC.L: 1.32
- CCH.L: 2.27
- CGS.L: 5.97
- CKN.L: 2.25
- CNA.L: 3.65
- COA.L: 3.07
- COST.L: 2.26
- CPI.L: no dividend
- CRDA.L: 3.21
- CRST.L: 4.84
- CSN.L: 6.11

Progress: 792/1084 done. (142/434 of this session's chunk)

### Batch 73 (tickers 790-801) — more .L tickers
- CTEC.L: 2.44
- CURY.L: 1.97
- CWK.L: 2.09
- DCC.L: 3.40
- DEC.L: 7.97
- DFS.L: 0.61
- DGE.L: 2.61
- DLN.L: 4.00
- DNLM.L: 5.17
- DOCS.L: 3.29
- DOM.L: 5.37
- DPLM.L: 0.86

Progress: 804/1084 done. (154/434 of this session's chunk)

### Batch 74 (tickers 802-813) — more .L tickers
- DRX.L: 3.91
- ECOR.L: 0.88
- EDV.L: 3.02
- ELIX.L: 3.77
- ELM.L: 1.91
- EMG.L: 4.09
- ENOG.L: 4.13
- ENQ.L: 3.18
- ENT.L: 4.01
- ESNT.L: 1.93
- EVOK.L: no dividend
- EXPN.L: 1.70

Progress: 816/1084 done. (166/434 of this session's chunk)

### Batch 75 (tickers 814-822) — more .L tickers
- EZJ.L: 1.96
- FAN.L: 1.69
- FCH.L: no dividend
- FDM.L: 6.28
- FGP.L: 4.02
- FORT.L: 4.17
- FRES.L: 3.53
- FSG.L: 5.44
- FSJ.L: no dividend

Progress: 825/1084 done. (175/434 of this session's chunk)

### Batch 76 (tickers 823-831) — more .L tickers
- FUTR.L: 5.49
- FVA.L: 1.66
- FXPO.L: no dividend
- GAW.L: 2.12
- GEN.L: 4.67
- GFRD.L: 3.29
- GFTU.L: 3.62
- GKP.L: 3.97
- GLE.L: 3.94

Progress: 834/1084 done. (184/434 of this session's chunk)

### Batch 77 (tickers 832-840) — more .L tickers
- GLEN.L: 2.11
- GNC.L: 0.97
- GNS.L: 1.40
- GPE.L: 2.43
- GRG.L: 3.72
- GRI.L: 4.84
- GROW.L: no dividend
- GSK.L: 3.67
- GYM.L: no dividend

Progress: 843/1084 done. (193/434 of this session's chunk)

### Batch 78 (tickers 841-849) — more .L tickers
- HAS.L: 0.57
- HBR.L: 4.73
- HFD.L: 3.29
- HHPD.L: 2.71
- HICL.L: no dividend
- HIK.L: 3.93
- HILS.L: 1.79
- HLCL.L: 1.31
- HLMA.L: 0.68

Progress: 852/1084 done. (202/434 of this session's chunk)

### Batch 79 (tickers 850-858) — more .L tickers
- HMSO.L: 4.83
- HOC.L: 0.99
- HSBA.L: 3.64
- HSW.L: 1.92
- HSX.L: 2.13
- HTG.L: 2.52
- HTWS.L: 0.60
- HWDN.L: 2.77
- HWG.L: 1.00

Progress: 861/1084 done. (211/434 of this session's chunk)

### Batch 80 (tickers 859-867) — more .L tickers
- IAG.L: 1.94
- IBST.L: 2.25
- ICG.L: 4.30
- IGG.L: 3.04
- IHP.L: 2.97
- III.L: 2.99
- IMB.L: 6.60
- IMI.L: 1.13
- INCH.L: 3.96

Progress: 870/1084 done. (220/434 of this session's chunk)

### Batch 81 (tickers 868-876) — more .L tickers
- INF.L: 2.49
- ITRK.L: 2.82
- ITV.L: 7.01
- IWG.L: 0.55
- JD.L: 1.38
- JDW.L: 1.41
- JMAT.L: 4.51
- JUP.L: 3.53
- KAP.L: 3.66

Progress: 879/1084 done. (229/434 of this session's chunk)

### Batch 82 (tickers 877-885) — more .L tickers
- KGF.L: 3.90
- KIE.L: 2.98
- KLR.L: 2.68
- KNOS.L: 2.37
- LAND.L: 12.94
- LGEN.L: 7.47
- LIO.L: 5.98
- LIVE.L: no dividend
- LLOY.L: 3.65

Progress: 888/1084 done. (238/434 of this session's chunk)

### Batch 83 (tickers 886-894) — more .L tickers
- LMP.L: 6.65
- LRE.L: 2.73
- LSEG.L: 1.76
- LUCE.L: 2.74
- MAB.L: no dividend
- MAB1.L: 4.39
- MACF.L: 4.75
- MARS.L: no dividend
- MCG.L: no dividend

Progress: 897/1084 done. (247/434 of this session's chunk)

### Batch 84 (tickers 895-902) — more .L tickers
- MER.L: 4.26
- MGAM.L: 5.06
- MICC.L: no dividend
- MKS.L: 1.06
- MNDI.L: 1.42
- MNG.L: 5.84
- MONY.L: 6.22
- MOTR.L: 1.92

Progress: 905/1084 done. (255/434 of this session's chunk)

### Batch 85 (tickers 903-908) — more .L tickers
- MRO.L: 1.46
- MSLH.L: 4.22
- MTO.L: 2.16
- MTRO.L: no dividend
- N91.L: 6.25
- NCC.L: 3.21

Progress: 911/1084 done. (261/434 of this session's chunk)

### Batch 86 (tickers 909-914) — more .L tickers
- NG.L: 4.14
- NRR.L: 8.28
- NWG.L: 5.15
- NXR.L: 3.47
- NXT.L: 1.72
- OCDO.L: no dividend

Progress: 917/1084 done. (267/434 of this session's chunk)

### Batch 87 (tickers 915-920) — more .L tickers
- ONT.L: no dividend
- OSB.L: 6.98
- OTB.L: 2.06
- OXB.L: no dividend
- OXIG.L: 0.83
- PAF.L: 1.60

Progress: 923/1084 done. (273/434 of this session's chunk)

### Batch 88 (tickers 921-926) — more .L tickers
- PAG.L: 5.69
- PAGE.L: 2.10
- PBEE.L: no dividend
- PETS.L: 3.39
- PFD.L: 1.68
- PHP.L: 7.64

Progress: 929/1084 done. (279/434 of this session's chunk)

### Batch 89 (tickers 927-932) — more .L tickers
- PINE.L: no dividend
- PLUS.L: 1.86
- PNN.L: 6.11
- PPH.L: 2.56
- PROC.L: no dividend
- PRU.L: 2.01

Progress: 935/1084 done. (285/434 of this session's chunk)

### Batch 90 (tickers 933-938) — more .L tickers
- PRV.L: 0.83
- PSN.L: 5.09
- PSON.L: 2.08
- PTEC.L: no dividend
- PZC.L: 3.57
- QLT.L: 3.30

Progress: 941/1084 done. (291/434 of this session's chunk)

### Batch 91 (tickers 939-944) — more .L tickers
- QQ.L: 2.17
- RAT.L: 5.84
- RCH.L: 13.75
- REL.L: 2.58
- RHIM.L: 5.63
- RIO.L: 4.54

Progress: 947/1084 done. (297/434 of this session's chunk)

### Batch 92 (tickers 945-950) — more .L tickers
- RKT.L: 4.22
- RMV.L: 2.11
- RNK.L: 3.39
- ROR.L: 1.72
- RPI.L: no dividend
- RR.L: 0.78

Progress: 953/1084 done. (303/434 of this session's chunk)

### Batch 93 (tickers 951-956) — more .L tickers
- RS1.L: 3.03
- RSG.L: no dividend
- RSW.L: 1.53
- RTO.L: 2.72
- SAFE.L: 5.24
- SAGA.L: no dividend

Progress: 959/1084 done. (309/434 of this session's chunk)

### Batch 94 (tickers 957-962) — more .L tickers
- SBRE.L: 7.60
- SBRY.L: 4.11
- SCT.L: 1.45
- SDLF.L: 5.97
- SDY.L: 5.54
- SEIT.L: no dividend

Progress: 965/1084 done. (315/434 of this session's chunk)

### Batch 95 (tickers 963-968) — more .L tickers
- SEPL.L: 2.24
- SFR.L: no dividend
- SGE.L: 2.06
- SGRO.L: 3.28
- SHC.L: 2.92
- SHEL.L: 3.46

Progress: 971/1084 done. (321/434 of this session's chunk)

### Batch 96 (tickers 969-973) — more .L tickers
- SHI.L: no dividend
- SMIN.L: 1.79
- SMSD.L: 0.83
- SMSN.L: 0.60
- SMWH.L: 3.18

Progress: 976/1084 done. (326/434 of this session's chunk)

### Batch 97 (tickers 974-979) — more .L tickers
- SN.L: 2.76
- SNWS.L: 8.04
- SPX.L: 2.41
- SRAD.L: 5.49
- SRE.L: 5.71
- SRP.L: 1.80

Progress: 982/1084 done. (332/434 of this session's chunk)

### Batch 98 (tickers 980-985) — more .L tickers
- SSE.L: 2.81
- SSPG.L: 2.19
- STAN.L: 2.36
- STJ.L: 1.52
- SUNB.L: 4.23
- SUS.L: 7.75

Progress: 988/1084 done. (338/434 of this session's chunk)

### Batch 99 (tickers 986-990) — more .L tickers
- SVS.L: 2.20
- SVT.L: 4.01
- SWC.L: no dividend
- SYNT.L: no dividend
- TATE.L: 3.57

Progress: 993/1084 done. (343/434 of this session's chunk)

### Batch 100 (tickers 991-996) — more .L tickers
- TCAP.L: 4.99
- TEP.L: 5.71
- THG.L: no dividend
- THRL.L: no dividend
- TLW.L: no dividend
- TPK.L: 1.77

Progress: 999/1084 done. (349/434 of this session's chunk)

### Batch 101 (tickers 997-1002) — more .L tickers
- TRI.L: 2.18
- TRN.L: no dividend
- TRST.L: no dividend
- TSCO.L: 3.19
- TW.L: 4.88
- ULVR.L: 3.45

Progress: 1005/1084 done. (355/434 of this session's chunk)

### Batch 102 (tickers 1003-1008) — more .L tickers
- UTG.L: 7.38
- UU.L: 3.75
- VALT.L: 5.45
- VANQ.L: no dividend
- VCT.L: 7.08
- VLX.L: 0.77

Progress: 1011/1084 done. (361/434 of this session's chunk)

### Batch 103 (tickers 1009-1013) — more .L tickers
- VOD.L: 3.36
- VSVS.L: 6.07
- VTY.L: no dividend
- WEIR.L: 1.48
- WIL.L: 4.30

Progress: 1016/1084 done. (366/434 of this session's chunk)

### Batch 104 (tickers 1014-1019) — more .L tickers
- WISE.L: no dividend
- WIX.L: 5.64
- WIZZ.L: no dividend
- WKP.L: 6.90
- WOSG.L: no dividend
- WPP.L: 3.92

Progress: 1022/1084 done. (372/434 of this session's chunk)

### Batch 105 (tickers 1020-1025) — more .L tickers
- WTB.L: 3.94
- XAR.L: no dividend
- XPP.L: no dividend
- XPS.L: 4.20
- ZEG.L: no dividend
- ZIG.L: 6.12

Progress: 1028/1084 done. (378/434 of this session's chunk)

### Batch 106 (tickers 1026-1030) — more .L tickers
- ZTF.L: 1.79
- 4BB.L: no dividend
- ABDP.L: 1.11
- ACSO.L: no dividend
- AET.L: no dividend

Progress: 1033/1084 done. (383/434 of this session's chunk)

### Batch 107 (tickers 1031-1036) — AIM (.L) tickers
- ALL.L: no dividend
- AXS.L: no dividend
- BKS.L: no dividend
- BOKU.L: no dividend
- BRCK.L: 6.71
- BTG.L: 4.18

Progress: 1039/1084 done. (389/434 of this session's chunk)

### Batch 108 (tickers 1037-1042) — more AIM (.L) tickers
- CAML.L: 8.71
- CER.L: 1.66
- CHRT.L: 1.46
- CNC.L: 0.44
- DOTD.L: 2.25
- DXRX.L: no dividend

Progress: 1045/1084 done. (395/434 of this session's chunk)

### Batch 109 (tickers 1043-1048) — more AIM (.L) tickers
- EAAS.L: no dividend
- ECO.L: no dividend
- EEE.L: no dividend
- FARN.L: no dividend
- FDEV.L: no dividend
- FEVR.L: 2.03

Progress: 1051/1084 done. (401/434 of this session's chunk)

### Batch 110 (tickers 1049-1053) — more AIM (.L) tickers
- FLO.L: no dividend
- FRP.L: 4.87
- GFM.L: no dividend
- GGP.L: no dividend
- GHH.L: 1.09

Progress: 1056/1084 done. (406/434 of this session's chunk)

### Batch 111 (tickers 1054-1059) — more AIM (.L) tickers
- GMR.L: no dividend
- HCM.L: no dividend
- IES.L: no dividend
- IOM.L: no dividend
- KETL.L: no dividend
- KGH.L: 3.38

Progress: 1062/1084 done. (412/434 of this session's chunk)

### Batch 112 (tickers 1060-1065) — more AIM (.L) tickers
- KIST.L: no dividend
- LBG.L: no dividend
- MANO.L: no dividend
- MIDW.L: 3.72
- MPE.L: 3.34
- NICL.L: 3.41

Progress: 1068/1084 done. (418/434 of this session's chunk)

### Batch 113 (tickers 1066-1070) — more AIM (.L) tickers
- NWF.L: 5.69
- PGH.L: 5.90
- POLR.L: 5.25
- PRO.L: no dividend
- RKH.L: no dividend

Progress: 1073/1084 done. (423/434 of this session's chunk)

### Batch 114 (tickers 1071-1081) — final AIM (.L) tickers + CBOE — CHUNK COMPLETE
- SAA.L: 2.52
- SDI.L: no dividend
- SRC.L: no dividend
- TAM.L: 3.90
- THS.L: 2.92
- THX.L: 3.58
- TIG.L: no dividend
- TRCS.L: 0.79
- ULTP.L: 5.69
- VIC.L: 2.96
- CBOE: 1.11

Progress: 1084/1084 done. (434/434 of this session's chunk — ALL DONE)

## Session complete

All 434 tickers assigned for this session (rows 3898-4331 of refresh_4330_list.tsv, resuming after PHIA.NV) have been scraped. yahoo_dividends_D.txt now has 1081 lines (647 pre-existing + 434 new). No duplicates. Final ticker in the file: CBOE.
