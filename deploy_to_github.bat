@echo off
echo 🚀 Deploying Soil Transmitted Diseases TLM to GitHub...
echo ===================================================

echo.
echo 📋 Step 1: Checking Git status...
git status

echo.
echo 📋 Step 2: Adding all files to Git...
git add .

echo.
echo 📋 Step 3: Committing changes...
git commit -m "Complete STH TLM package with Indian context visuals and PPTX files

- Added 6 comprehensive educational modules
- Created 7 Indian context PPTX presentations (158+ slides)
- Added visual assets with state-wise prevalence data
- Included complete assessment and practical materials
- Set up CI/CD pipeline for automated validation
- Added comprehensive documentation and references"

echo.
echo 📋 Step 4: Checking remote repository...
git remote -v

echo.
echo 📋 Step 5: Pushing to GitHub...
git push origin main

echo.
echo ✅ Deployment complete!
echo.
echo 🌟 Your STH TLM package is now live on GitHub!
echo 📁 Repository: https://github.com/hssling/Soil_Transmitted_Diseases_TLM
echo.
echo 📊 Package includes:
echo   - 6 educational modules (200+ pages)
echo   - 7 PPTX presentations (158+ slides)
echo   - Indian context visual assets
echo   - Complete assessment framework
echo   - CI/CD automation
echo   - MIT license for educational use
echo.
echo 🎯 Ready for medical education and public health training!
echo.
pause
