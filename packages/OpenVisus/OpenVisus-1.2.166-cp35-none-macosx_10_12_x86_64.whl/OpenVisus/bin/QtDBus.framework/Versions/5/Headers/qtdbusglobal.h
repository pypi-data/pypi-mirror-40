/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtDBus module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 2.0 or (at your option) the GNU General
** Public license version 3 or any later version approved by the KDE Free
** Qt Foundation. The licenses are as published by the Free Software
** Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-2.0.html and
** https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#ifndef QTDBUSGLOBAL_H
#define QTDBUSGLOBAL_H

#include <QtCore/qglobal.h>
#include <QtCore/qmetatype.h>
#include <QtCore/qvariant.h>

#ifndef Q_MOC_RUN
# define Q_NOREPLY
#endif

#ifdef Q_CC_MSVC
#include <QtCore/qlist.h>
#include <QtCore/qset.h>
#if QT_DEPRECATED_SINCE(5, 5)
#include <QtCore/qhash.h>
#endif
#include <QtCore/qvector.h>
#endif

QT_BEGIN_NAMESPACE

#ifndef QT_NO_DBUS

#ifndef QT_STATIC
#  if defined(QT_BUILD_DBUS_LIB)
#    define Q_DBUS_EXPORT Q_DECL_EXPORT
#  else
#    define Q_DBUS_EXPORT Q_DECL_IMPORT
#  endif
#else
#  define Q_DBUS_EXPORT
#endif

#endif // QT_NO_DBUS

QT_END_NAMESPACE

#endif
