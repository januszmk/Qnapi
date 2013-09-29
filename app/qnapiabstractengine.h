/*****************************************************************************
** QNapi
** Copyright (C) 2008-2009 Krzemin <pkrzemin@o2.pl>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
*****************************************************************************/

#ifndef __QNAPIABSTRACTENGINE__H__
#define __QNAPIABSTRACTENGINE__H__

#include <QString>
#include <QFileInfo>
#include <QFile>
#include <QTextCodec>
#include <QTextStream>
#include <QIcon>
#include <QPixmap>

#include <ctime>

#include "qnapiconfig.h"
#include "qnapisubtitleinfo.h"

class QNapiAbstractEngine
{
public:

	// destruktor
    virtual ~QNapiAbstractEngine();

	// ustawia sciezke do pliku filmowego
	void setMoviePath(const QString & path);
	// zwraca sciezke do pliku filmowego
	QString moviePath();
	// ustawia sciezke do pliku z napisami
	void setSubtitlesPath(const QString & path);
	// zwraca sciezke do pliku z napisami
	QString subtitlesPath();

	// dopasowuje napisy do pliku z filmem
  /*  virtual*/ bool match();

    // konwersja na srt
    virtual bool convert();

	// usuwa linie z pliku zawierajace conajmniej jedno z podanej listy slow
	bool ppRemoveLinesContainingWords(QStringList wordList);
	// zmienia uprawnienia do pliku z napisami
	bool ppChangeSubtitlesPermissions(QFile::Permissions permissions);

	// powinna zwracac nazwe modulu
	virtual QString engineName() = 0;
	// powinna zwracac informacje nt. modulu (prawa autorskie itp.)
	virtual QString engineInfo() = 0;
	// zwraca ikone silnika pobierania
	virtual QIcon engineIcon() = 0;

	// powinna obliczac i zwracac sume kontrolna pliku filmowego,
	// a takze ustawiac wartosc zmiennej checkSym
	virtual QString checksum(QString filename = "") = 0;
	// szuka napisow w podanym jezyku
	virtual bool lookForSubtitles(QString lang) = 0;
	// zwraca liste dostepnych napisow
	virtual QList<QNapiSubtitleInfo> listSubtitles() = 0;
	// powinna pobierac napisy do filmu i zapisywac w jakims pliku tymczasowym
	virtual bool download(int idx) = 0;
    // powinna rozpakowywac pobrane napisy
	virtual bool unpack() = 0;
	// powinna czyscic pliki tymczasowe itd.
    virtual void cleanup();

    void pp();
protected:

	// sciezka do pliku filmowego
	QString movie;
	// sciezka do napisow (zazwyczaj taka sama jak do napisow z innym rozszerzeniem)
	QString subtitles;
	// sciezka do tymczasowego pliku z napisami
	QString subtitlesTmp;
    // sciezka do spakowanego pliku napisow
    QString tmpPackedFile;
	// sciezka do katalogu tymczasowego
	QString tmpPath;
    // sciezka do pliku skryptu konwertujacego
    QString scriptPath;
	// suma kontrolna pliku filmowego
	QString checkSum;
	// okresla czy uzytkownik wylaczyl wykonywanie kopii zapasowej, gdy napisy do
	// zadanego filmu juz istnieja
	bool noBackup;

	// konstruktor klasy
    QNapiAbstractEngine(const QString & movieFile = "", const QString & subtitlesFile = "");

	// generuje nazwe dla pliku tymczasowego
	QString generateTmpFileName();

};

#endif
