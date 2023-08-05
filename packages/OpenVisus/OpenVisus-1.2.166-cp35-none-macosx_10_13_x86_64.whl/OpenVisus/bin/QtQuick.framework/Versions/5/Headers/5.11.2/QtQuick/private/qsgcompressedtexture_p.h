/****************************************************************************
**
** Copyright (C) 2017 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtQuick module of the Qt Toolkit.
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

#ifndef QSGCOMPRESSEDTEXTURE_P_H
#define QSGCOMPRESSEDTEXTURE_P_H

//
//  W A R N I N G
//  -------------
//
// This file is not part of the Qt API.  It exists purely as an
// implementation detail.  This header file may change from version to
// version without notice, or even be removed.
//
// We mean it.
//

#include <QSGTexture>
#include <QtQuick/private/qsgcontext_p.h>
#include <QQuickTextureFactory>
#include <QOpenGLFunctions>

QT_BEGIN_NAMESPACE

struct Q_QUICK_PRIVATE_EXPORT QSGCompressedTextureData
{
    QByteArray logName;
    QByteArray data;
    QSize size;
    uint format = 0;
    int dataOffset = 0;
    int dataLength = 0;
    bool hasAlpha = false;

    bool isValid() const;
    int sizeInBytes() const;
};

Q_QUICK_PRIVATE_EXPORT QDebug operator<<(QDebug, const QSGCompressedTextureData *);


class Q_QUICK_PRIVATE_EXPORT QSGCompressedTexture : public QSGTexture
{
    Q_OBJECT
public:
    typedef QSharedPointer<QSGCompressedTextureData> DataPtr;

    QSGCompressedTexture(const DataPtr& texData);
    virtual ~QSGCompressedTexture();

    int textureId() const override;
    QSize textureSize() const override;
    bool hasAlphaChannel() const override;
    bool hasMipmaps() const override;

    void bind() override;

    const QSGCompressedTextureData *textureData();

    static bool formatIsOpaque(quint32 glTextureFormat);

protected:
    DataPtr m_textureData;
    QSize m_size;
    mutable uint m_textureId = 0;
    bool m_hasAlpha = false;
    bool m_uploaded = false;
};

namespace QSGAtlasTexture {
    class Manager;
}

class Q_QUICK_PRIVATE_EXPORT QSGCompressedTextureFactory : public QQuickTextureFactory
{
public:
    QSGCompressedTextureFactory(const QSGCompressedTexture::DataPtr& texData);
    QSGTexture *createTexture(QQuickWindow *) const override;
    int textureByteCount() const override;
    QSize textureSize() const override;

protected:
    QSGCompressedTexture::DataPtr m_textureData;
private:
    friend class QSGAtlasTexture::Manager;
};

QT_END_NAMESPACE

#endif // QSGCOMPRESSEDTEXTURE_P_H
